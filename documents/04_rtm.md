# 04. Matriz de Rastreabilidade de Requisitos (RTM)

## 1. Requisitos Funcionais (RF)

| ID | Descrição | Status | Validação |
| :--- | :--- | :--- | :--- |
| RF01 | Extração de Object Storage (MinIO) | ✅ | Logs do `ingestion-engine` |
| RF02 | Validação e Carga em Staging OLAP | ✅ | Tabelas no ClickHouse (`olist.ingestion`) |
| RF03 | Transformação de Dados (Modelagem) | ✅ | Tabela `olist.fct_orders` via dbt |
| RF04 | Persistência Idempotente e Atomicidade | ✅ | Logs de reprocessamento sem duplicidade |
| RF05 | Auditoria de Carga e Transformação | ✅ | Logs estruturados em JSON |
| RF06 | Alerta de Falha no Pipeline | ✅ | Circuit Breaker em `ingest.py` |
| RF07 | Dashboard Analítico | ✅ | Streamlit rodando na porta 8501 |

## 2. Requisitos Não Funcionais (RNF)

| ID | Descrição | Status | Validação |
| :--- | :--- | :--- | :--- |
| RNF-01 | Velocidade de Ingestão | ✅ | < 5 min para 100k registros (verificado via logs) |
| RNF-02 | Latência de Query | ✅ | k6: p(95) = 36.26ms (< 1s) |
| RNF-03 | Integridade de Dados | ✅ | dbt tests (Unique, Not Null) - 4/4 PASS |
| RNF-04 | Tempo de Recovery | ✅ | Estrutura de DLQ em MinIO |
| RNF-05 | Modularidade | ✅ | Modelos dbt organizados em staging/marts |
| RNF-06 | Isolamento via Docker | ✅ | Stack completa via Docker Compose em < 1 min |
| RNF-07 | Segurança | ✅ | Controle de acesso via env vars e secrets |
