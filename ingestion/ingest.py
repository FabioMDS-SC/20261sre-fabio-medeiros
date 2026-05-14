import os
import boto3
import pandas as pd
import json
from datetime import datetime
import clickhouse_connect
from dotenv import load_dotenv
import io

load_dotenv()

# Configurações
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'admin123')
BUCKET_NAME = 'olistproject'
PREFIX = 'archive/'

CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER', 'default')
CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', 'password123')
CLICKHOUSE_DB = os.getenv('CLICKHOUSE_DB', 'olist')

def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )

def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        user=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DB
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
    print("Tabela 'ingestion' verificada/criada.")

def ingest_files():
    s3 = get_minio_client()
    ch_client = get_clickhouse_client()
    
    setup_database(ch_client)
    
    # Listar objetos no MinIO
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    
    if 'Contents' not in response:
        print(f"Nenhum arquivo encontrado em {BUCKET_NAME}/{PREFIX}")
        return

    for obj in response['Contents']:
        file_key = obj['Key']
        if not file_key.endswith('.csv'):
            continue
            
        print(f"Processando arquivo: {file_key}")
        
        # Ler arquivo do MinIO
        csv_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
        body = csv_obj['Body'].read()
        
        # Usar Pandas para ler o CSV (mais fácil para converter em JSON)
        df = pd.read_csv(io.BytesIO(body))
        
        # Preparar dados para o ClickHouse
        # O usuário quer: unixtime, data (json), tag (filename)
        now = datetime.now()
        tag = file_key.split('/')[-1]
        
        rows_to_insert = []
        for _, row in df.iterrows():
            json_data = row.to_json()
            rows_to_insert.append([now, json_data, tag])
            
        # Inserir no ClickHouse
        if rows_to_insert:
            ch_client.insert(f"{CLICKHOUSE_DB}.ingestion", rows_to_insert, column_names=['unixtime', 'data', 'tag'])
            print(f"Inseridas {len(rows_to_insert)} linhas do arquivo {tag}.")

if __name__ == "__main__":
    ingest_files()
