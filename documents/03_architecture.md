# 03. Arquitetura do Sistema (RM-ODP)

Este documento descreve a arquitetura do pipeline de processamento de pedidos utilizando os cinco pontos de vista do framework RM-ODP, focado em uma infraestrutura **Local com Banco OLAP e Object Storage**.

## 1. Enterprise Viewpoint (Ponto de Vista de Negócio)
**Propósito:** Modernizar a ingestão de pedidos da Olist utilizando uma arquitetura analítica moderna rodando localmente.
- **Objetivo:** Processar 100k pedidos/dia em < 4h (RNF-02) com foco em performance analítica (OLAP).
- **Stakeholders:** Time de Analytics e Engenharia de Dados.
- **Processo de Negócio:** Depósito no Object Storage local (MinIO) -> Ingestão para Staging Local -> Carga no Banco OLAP (ClickHouse) -> Transformação (dbt) -> Dashboard (Grafana).

## 2. Information Viewpoint (Ponto de Vista de Informação)
**Foco:** Ciclo de vida dos dados analíticos.
- **Camada Bronze (Raw/Object Storage):** Arquivos CSV originais persistidos no MinIO.
- **Camada Silver (Staging/OLAP):** Dados limpos e tipados em tabelas MergeTree do ClickHouse.
- **Camada Gold (Analytics/Transformation):** Visões agregadas e tabelas de fatos/dimensões transformadas via SQL.
- **Metadados:** Logs de execução e métricas de compressão/performance do OLAP.

## 3. Computational Viewpoint (Ponto de Vista Computacional)
**Foco:** Decomposição funcional.
- **Serviço de Ingestão:** Script Python que extrai dados do MinIO e carrega no ClickHouse (utilizando buffers ou carga direta por arquivo).
- **Banco OLAP:** ClickHouse responsável por armazenamento colunar de alta performance.
- **Motor de Transformação:** dbt (data build tool) ou scripts SQL para processar dados dentro do ClickHouse.
- **Interface de Dashboard:** Grafana conectado ao ClickHouse para visualização em tempo real das métricas.

## 4. Engineering Viewpoint (Ponto de Vista de Engenharia)
**Foco:** Infraestrutura local via Docker.
- **Object Storage Local:** MinIO (API compatível com S3) rodando em container.
- **Banco Analítico:** ClickHouse (Engine MergeTree) para consultas rápidas em grandes volumes.
- **Orquestrador de Containers:** Docker Compose gerenciando a rede e volumes.
- **Agendamento:** Cron ou script Python de controle para disparar o lote diário.

## 5. Technology Viewpoint (Ponto de Vista de Tecnologia)
**Stack Tecnológica Local:**
- **Object Storage:** MinIO.
- **Banco OLAP:** ClickHouse.
- **Ingestão/ETL:** Python (Pandas/DuckDB como motor de carga).
- **Transformação:** dbt-clickhouse ou SQL nativo.
- **Visualização:** Grafana.
- **Infraestrutura:** Docker & Docker Compose.

---

## 🏗️ Architecture Decision Records (ADRs)

### ADR 001: ClickHouse como Banco OLAP
- **Contexto:** Necessidade de performance analítica superior para consultas em 100k+ registros diários.
- **Decisão:** Utilizar ClickHouse em vez de PostgreSQL.
- **Consequências:** Ganho massivo em velocidade de agregação e compressão de dados, embora exija uma modelagem colunar específica.

### ADR 002: MinIO para Simular Object Storage Local
- **Contexto:** Garantir que o pipeline seja compatível com padrões de mercado (S3) mesmo rodando localmente.
- **Decisão:** Utilizar MinIO.
- **Consequências:** Facilidade de migração para nuvem no futuro e desacoplamento entre a origem do arquivo e o processamento.

### ADR 003: dbt para Camada de Transformação
- **Contexto:** Necessidade de versionar e testar as transformações SQL.
- **Decisão:** Utilizar dbt (data build tool).
- **Consequências:** Melhor governança de dados, documentação automática e linhagem de dados clara.

### ADR 004: Ingestão Local via DuckDB -> ClickHouse
- **Contexto:** Otimizar a velocidade de transferência entre o CSV/MinIO e o banco final.
- **Decisão:** Utilizar DuckDB como motor intermediário de leitura para "pushar" dados para o ClickHouse.
- **Consequências:** Redução drástica no tempo de ingestão comparado a inserts linha a linha tradicionais.

---
**Nota:** Este documento reflete o fluxo: Object Storage -> Ingestão -> Local -> Banco OLAP -> Transformação -> Dashboard.
