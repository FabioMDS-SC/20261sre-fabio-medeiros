# GEMINI.md

## Projeto: Modernização do Pipeline de Ingestão de Dados (Olist)

Este projeto tem como objetivo a estabilização e modernização do pipeline de ingestão de dados da Olist, utilizando uma arquitetura analítica moderna e local. O fluxo processa arquivos CSV de um Object Storage local (MinIO) para um Banco OLAP (ClickHouse), com transformações via dbt e visualização no Grafana.

## 📂 Estrutura de Diretórios

O projeto está organizado para suportar tanto a documentação técnica quanto a automação via agentes de IA.

### 📄 `documents/` (Documentação do Projeto)
Este diretório contém toda a documentação oficial do ciclo de vida do software.
- `00_index.md`: Ponto de entrada e índice de toda a documentação.
- `01_functional_requirements.md`: Requisitos Funcionais (RF) focados em OLAP.
- `02_non_functional_requirements.md`: Requisitos Não Funcionais (RNF) analíticos.
- `03_architecture.md`: Arquitetura Local (Object Storage -> OLAP -> Transformação).
- `04_rtm.md`: Matriz de Rastreabilidade de Requisitos (RTM).
- `08_system_design.md`: Detalhes de design do sistema e componentes Docker.
- `09_local_execution_logs.md`: Registro de comandos e sessões de execução local.

### 🤖 `agents/` (Framework de Agentes)
...

## 🏗️ Tecnologias Principais (Stack OLAP Local)
- **Object Storage:** MinIO (API compatível com S3).
- **Ingestão:** Python / DuckDB.
- **Banco OLAP:** ClickHouse (Colunar).
- **Transformação:** dbt (data build tool).
- **Visualização:** Grafana.
- **Orquestração de Infra:** Docker Compose.
