import pytest
import io
import pandas as pd
from ingestion.ingest import is_already_ingested, read_from_minio, write_to_clickhouse

def test_is_already_ingested_true(mocker):
    # Mock do cliente ClickHouse
    mock_ch = mocker.Mock()
    mock_ch.query.return_value.first_row = [1]
    
    assert is_already_ingested(mock_ch, "test.csv") is True
    mock_ch.query.assert_called_once()

def test_is_already_ingested_false(mocker):
    mock_ch = mocker.Mock()
    mock_ch.query.return_value.first_row = [0]
    
    assert is_already_ingested(mock_ch, "new.csv") is False

def test_read_from_minio_success(mocker):
    mock_s3 = mocker.Mock()
    mock_s3.get_object.return_value = {
        'Body': mocker.Mock(read=mocker.Mock(return_value=b"col1,col2\nval1,val2"))
    }
    
    content = read_from_minio(mock_s3, "bucket", "key.csv")
    assert content == b"col1,col2\nval1,val2"

def test_write_to_clickhouse_call(mocker):
    mock_ch = mocker.Mock()
    rows = [[pd.Timestamp.now(), '{"a":1}', 'file.csv']]
    
    write_to_clickhouse(mock_ch, "table", rows)
    mock_ch.insert.assert_called_once_with("table", rows, column_names=['unixtime', 'data', 'tag'])

def test_json_data_conversion():
    # Teste de lógica pura: conversão para JSON via Pandas
    df = pd.DataFrame([{"id": 1, "name": "Olist"}])
    json_data = df.iloc[0].to_json()
    assert '"id":1' in json_data
    assert '"name":"Olist"' in json_data
