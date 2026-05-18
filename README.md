# Olist Data Pipeline Modernization

Este projeto implementa um pipeline de dados moderno e local para os dados da Olist.

## Stack Tecnológica
- **MinIO**: Object Storage compatível com S3.
- **ClickHouse**: Banco de dados OLAP colunar.
- **dbt**: Transformação de dados.
- **Streamlit**: Dashboard de visualização.
- **k6**: Testes de carga.

## Como Executar

### 1. Subir a infraestrutura
```bash
docker-compose up -d
```

### 2. Executar Testes de Carga (k6)
```bash
docker run --rm --network olist_network -v $(pwd)/tests:/tests grafana/k6 run /tests/load_test.js
```

### 3. Executar Testes de Dados (dbt)
```bash
docker exec dbt-runner dbt test --profiles-dir .
```

### 4. Acessar o Dashboard
O Streamlit estará disponível em `http://localhost:8501`.

## Documentação
A documentação completa está disponível na pasta `documents/`.
- `04_rtm.md`: Matriz de Rastreabilidade.
- `05_test_plan_load.md`: Resultados dos testes de carga.
- `09_local_execution_logs.md`: Logs de execução.
