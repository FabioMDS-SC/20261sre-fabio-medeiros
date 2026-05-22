import boto3
import pandas as pd
import clickhouse_connect
import io
from datetime import datetime

def ingest_files():
    CH_HOST = "10.0.1.96"
    CH_USER = "admin"
    CH_PASS = "password123"
    CH_DB = "olist"
    BUCKET = "olist-raw-975049965631-us-east-1"

    print("Pipeline iniciado.")
    ch_client = clickhouse_connect.get_client(host=CH_HOST, user=CH_USER, password=CH_PASS, database=CH_DB)
    s3 = boto3.client('s3', region_name='us-east-1')
    
    response = s3.list_objects_v2(Bucket=BUCKET)
    
    for obj in response.get('Contents', []):
        key = obj['Key']
        if not key.endswith('.csv') or 'deploy/' in key:
            continue
        
        print(f"Processando {key}...")
        csv_obj = s3.get_object(Bucket=BUCKET, Key=key)
        df = pd.read_csv(io.BytesIO(csv_obj['Body'].read()))
        
        now = datetime.now()
        rows = [[now, row.to_json(), key] for _, row in df.iterrows()]
        
        ch_client.insert('ingestion', rows, column_names=['unixtime', 'data', 'tag'])
        print(f"Sucesso: {key} ({len(rows)} linhas)")

if __name__ == "__main__":
    ingest_files()
