import os
import boto3
import pandas as pd
import json
import logging
from datetime import datetime
import clickhouse_connect
from dotenv import load_dotenv
import io
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from botocore.config import Config
from botocore.exceptions import ClientError

load_dotenv()

# Configuração de Logging Estruturado (Tática de Observabilidade)
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

logger = logging.getLogger("ingestion-engine")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Configurações
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'admin123')
BUCKET_NAME = os.getenv('MINIO_BUCKET', 'olist-raw')
FAILED_PREFIX = 'olist-failed/' # Prefixo para DLQ
PREFIX = os.getenv('MINIO_PREFIX', '')

CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER', 'default')
CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', 'password123')
CLICKHOUSE_DB = os.getenv('CLICKHOUSE_DB', 'olist')

# Configuração de Timeouts para Boto3
s3_config = Config(
    connect_timeout=5,
    read_timeout=10,
    retries={'max_attempts': 0}
)

def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=s3_config
    )

def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        user=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DB,
        connect_timeout=10
    )

def setup_database(ch_client):
    ch_client.command(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DB}")
    ch_client.command(f"""
        CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB}.ingestion (
            unixtime DateTime,
            data String,
            tag String
        ) ENGINE = MergeTree()
        ORDER BY (unixtime, tag)
    """)
    logger.info("Tabela 'ingestion' verificada/criada.")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ClientError, Exception))
)
def read_from_minio(s3, bucket, key):
    csv_obj = s3.get_object(Bucket=bucket, Key=key)
    return csv_obj['Body'].read()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def write_to_clickhouse(ch_client, table, rows):
    ch_client.insert(table, rows, column_names=['unixtime', 'data', 'tag'])

def is_already_ingested(ch_client, tag):
    result = ch_client.query(f"SELECT count() FROM {CLICKHOUSE_DB}.ingestion WHERE tag = '{tag}'")
    return result.first_row[0] > 0

def move_to_dlq(s3, bucket, key):
    """Move arquivo para o prefixo de falha (Tática DLQ)."""
    filename = key.split('/')[-1]
    new_key = f"{FAILED_PREFIX}{filename}"
    try:
        s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': key}, Key=new_key)
        s3.delete_object(Bucket=bucket, Key=key)
        logger.warning(f"Arquivo movido para DLQ: {new_key}")
    except Exception as e:
        logger.error(f"Falha ao mover arquivo para DLQ: {e}")

def ingest_files():
    s3 = get_minio_client()
    ch_client = get_clickhouse_client()
    
    setup_database(ch_client)
    
    # Garantir que o bucket existe
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
    except:
        logger.info(f"Criando bucket: {BUCKET_NAME}")
        s3.create_bucket(Bucket=BUCKET_NAME)
    
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    
    if 'Contents' not in response:
        logger.info(f"Nenhum arquivo encontrado em {BUCKET_NAME}/{PREFIX}")
        return

    # Tática de Circuit Breaker
    error_count = 0
    MAX_ERRORS = 3

    for obj in response['Contents']:
        file_key = obj['Key']
        if not file_key.endswith('.csv') or file_key.startswith(FAILED_PREFIX):
            continue
            
        tag = file_key.split('/')[-1]
        
        if is_already_ingested(ch_client, tag):
            logger.info(f"Arquivo {tag} já processado. Pulando.")
            continue
            
        if error_count >= MAX_ERRORS:
            logger.critical("Circuit Breaker ativado: Limite de erros atingido. Interrompendo pipeline.")
            break

        logger.info(f"Processando arquivo: {file_key}")
        
        try:
            body = read_from_minio(s3, BUCKET_NAME, file_key)
            df = pd.read_csv(io.BytesIO(body))
            
            now = datetime.now()
            rows_to_insert = []
            for _, row in df.iterrows():
                json_data = row.to_json()
                rows_to_insert.append([now, json_data, tag])
                
            if rows_to_insert:
                write_to_clickhouse(ch_client, f"{CLICKHOUSE_DB}.ingestion", rows_to_insert)
                logger.info(f"Sucesso: Inseridas {len(rows_to_insert)} linhas de {tag}.")
                error_count = 0 # Reset do contador de erros em caso de sucesso
        except Exception as e:
            error_count += 1
            logger.error(f"Erro ao processar {tag}: {e}. Erros consecutivos: {error_count}")
            move_to_dlq(s3, BUCKET_NAME, file_key)

if __name__ == "__main__":
    ingest_files()


if __name__ == "__main__":
    ingest_files()


if __name__ == "__main__":
    ingest_files()
