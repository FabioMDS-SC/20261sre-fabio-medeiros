# 01. Requisitos Funcionais (RF)

Este documento detalha as funcionalidades necessárias para a modernização do pipeline de ingestão de dados em ambiente **local com arquitetura OLAP**, garantindo que o sistema atenda aos objetivos analíticos.

## 👥 Atores do Sistema
- **Object Storage Local (MinIO):** Repositório de arquivos CSV brutos (Camada Bronze).
- **Serviço de Ingestão (Python/DuckDB):** Componente que move dados do Object Storage para o Banco OLAP.
- **Banco OLAP (ClickHouse):** Armazenamento colunar para análise de alto desempenho (Camada Silver/Gold).
- **Ferramenta de Transformação (dbt):** Motor de processamento para lógica de negócio e modelagem.
- **Visualizador (Streamlit):** Interface de consumo dos dados transformados.

## 🛠️ Requisitos de Ingestão e Processamento

### RF01: Extração de Object Storage (MinIO)
- **Descrição:** O sistema deve ler arquivos CSV depositados em buckets do MinIO de forma automatizada.
- **Prioridade:** Must-have
- **Critério de Aceitação:** Sucesso na conexão e leitura de arquivos via protocolo S3 local.

### RF02: Validação e Carga em Staging OLAP
- **Descrição:** O sistema deve validar o esquema dos arquivos e carregá-los em tabelas de staging no ClickHouse.
- **Prioridade:** Must-have
- **Critério de Aceitação:** Dados disponíveis no ClickHouse com tipos de dados colunares corretos.

### RF03: Transformação de Dados (Modelagem)
- **Descrição:** O sistema deve aplicar regras de negócio, agregações e deduplicação utilizando SQL dentro do Banco OLAP.
- **Prioridade:** Must-have
- **Critério de Aceitação:** Existência de tabelas finais (Gold) prontas para consumo analítico.

### RF04: Persistência Idempotente e Atomicidade
- **Descrição:** O sistema deve garantir que o reprocessamento de um lote não duplique dados, utilizando engines de merge do ClickHouse ou lógica de limpeza de staging.
- **Prioridade:** Must-have
- **Critério de Aceitação:** Consistência numérica entre o arquivo de origem e o banco final após reprocessamentos.

## 📊 Requisitos de Observabilidade e Visualização

### RF05: Auditoria de Carga e Transformação
- **Descrição:** Registro de logs detalhados para cada etapa (Ingestão -> Transformação).
- **Prioridade:** Must-have
- **Critério de Aceitação:** Logs consultáveis que mostrem o volume de dados em cada etapa do pipeline.

### RF06: Alerta de Falha no Pipeline
- **Descrição:** Notificação imediata em caso de erro na leitura do MinIO ou falha nos scripts dbt.
- **Prioridade:** Must-have
- **Critério de Aceitação:** Registro de erro com traceback completo disponível localmente.

### RF07: Dashboard Analítico
- **Descrição:** Disponibilização de painéis interativos no Streamlit consumindo diretamente do ClickHouse.
- **Prioridade:** Should-have
- **Critério de Aceitação:** Visualização de KPIs (pedidos por dia, status, etc.) com tempo de resposta < 2s.

---
**Nota:** Este documento foca no fluxo analítico: MinIO -> ClickHouse -> dbt -> Streamlit.
