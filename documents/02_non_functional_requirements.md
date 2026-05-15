# 02. Requisitos Não Funcionais (RNF)

Este documento define os requisitos de qualidade técnica para o pipeline analítico local, focados em performance de grandes volumes de dados (OLAP).

## 1. Eficiência de Desempenho (Performance Efficiency)
- **RNF-01: Velocidade de Ingestão (Ingestion Speed)**
    - **Descrição:** O sistema deve carregar 100k registros do MinIO para o ClickHouse rapidamente.
    - **SLO:** < 5 minutos para 100k registros.
    - **Prioridade:** Must-have

- **RNF-02: Tempo de Resposta Analítica (Query Latency)**
    - **Descrição:** Consultas complexas no Banco OLAP devem retornar dados para o dashboard quase instantaneamente.
    - **SLO:** < 1 segundo para 95% das queries agregadas.
    - **Prioridade:** Must-have

## 2. Confiabilidade (Reliability)
- **RNF-03: Integridade de Dados no OLAP**
    - **Descrição:** Garantir que a compressão colunar não afete a precisão dos dados.
    - **SLO:** 100% de acurácia comparado à origem.
    - **Prioridade:** Must-have

- **RNF-04: Recuperabilidade de Lote**
    - **Descrição:** Capacidade de limpar e reprocessar o lote diário no ClickHouse em caso de falha de transformação.
    - **SLO:** < 10 minutos para rollback e reinício.
    - **Prioridade:** Must-have

## 3. Manutenibilidade e Portabilidade
- **RNF-05: Modularidade de Transformação**
    - **Descrição:** As transformações devem ser modulares e documentadas via dbt.
    - **SLO:** 100% dos modelos SQL documentados no dbt docs.
    - **Prioridade:** Should-have

- **RNF-06: Isolamento via Docker**
    - **Descrição:** Toda a stack (MinIO, ClickHouse, Streamlit) deve rodar isolada em containers.
    - **SLO:** Provisionamento total via `docker-compose` em < 10 minutos.
    - **Prioridade:** Must-have

## 4. Segurança
- **RNF-07: Controle de Acesso ao Banco OLAP**
    - **Descrição:** Restrição de usuários e senhas para acesso ao ClickHouse e MinIO, mesmo localmente.
    - **SLO:** 100% de conformidade com secrets não expostos em código.
    - **Prioridade:** Must-have

---

## Tabela de Resumo de Requisitos Não Funcionais

| ID | Atributo | SLI (Métrica) | SLO (Meta) | Fonte de Medição | Prioridade |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RNF-01 | Performance | Tempo de Ingestão | < 5 min | Logs de ETL | Must-have |
| RNF-02 | Performance | Latência de Query | < 1s | ClickHouse System Logs | Must-have |
| RNF-03 | Confiabilidade | Integridade de Dados | 100% | dbt tests | Must-have |
| RNF-04 | Confiabilidade | Tempo de Recovery | < 10 min | Logs de Execução | Must-have |
| RNF-05 | Manutenibilidade | Documentação dbt | 100% | dbt docs | Should-have |
| RNF-06 | Portabilidade | Tempo de Setup | < 10 min | Docker Compose | Must-have |
| RNF-07 | Segurança | Gestão de Secrets | 100% | Auditoria de Env | Must-have |

---
**Nota:** Este documento prioriza a performance colunar e a reprodutibilidade local via Docker.
