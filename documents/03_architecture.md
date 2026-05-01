# 03. Arquitetura do Sistema (RM-ODP)

Este documento descreve a arquitetura do pipeline de processamento de pedidos utilizando os cinco pontos de vista do framework RM-ODP, garantindo rastreabilidade com os requisitos funcionais (RF) e não funcionais (RNF).

## 1. Enterprise Viewpoint (Ponto de Vista de Negócio)
**Propósito:** Modernizar a ingestão de pedidos da Olist para garantir integridade e escalabilidade.
- **Objetivo:** Processar 100k pedidos/dia em < 4h (RNF-02) com 100% de integridade (RNF-01).
- **Stakeholders:** Time de Dados e Operações Olist.
- **Processo de Negócio:** Detecção automática de novos arquivos (RF-01) -> Validação e Transformação (RF-02/03) -> Carga Idempotente (RF-04).

## 2. Information Viewpoint (Ponto de Vista de Informação)
**Foco:** Fluxo e semântica dos dados.
- **Entrada:** Arquivos de texto delimitados (CSV) com esquema definido (RF-02).
- **Estado de Transição (Staging):** Área temporária para limpeza e validação cruzada (RF-03, RNF-07).
- **Estado Final:** Tabelas relacionais normalizadas no repositório persistente (RF-04).
- **Metadados:** Logs de auditoria e métricas de execução (RF-05, RF-07, RNF-09).

## 3. Computational Viewpoint (Ponto de Vista Computacional)
**Foco:** Decomposição funcional e interfaces.
- **Interface de Ingestão:** Detecta e valida a estrutura do arquivo (Atende RF-01, RF-02, RNF-04).
- **Serviço de Transformação:** Implementa lógica de limpeza e carga em staging (Atende RF-03, RNF-03).
- **Serviço de Sincronização (Upsert):** Garante a atualização atômica e idempotente (Atende RF-04, RNF-07).
- **Serviço de Monitoramento:** Coleta métricas e dispara alertas (Atende RF-06, RF-07, RNF-05).

## 4. Engineering Viewpoint (Ponto de Vista de Engenharia)
**Foco:** Distribuição e infraestrutura lógica.
- **Orquestrador de Workflow:** Gerencia a máquina de estados, retentativas e tratamento de erros (RNF-06).
- **Executor de Containers:** Unidade de computação isolada para processamento intensivo (RNF-02, RNF-10).
- **Fila de Eventos:** Desacopla a origem de dados do processamento, garantindo resiliência (RNF-06).
- **Criptografia em Repouso/Trânsito:** Implementada em todos os pontos de armazenamento e comunicação (RNF-08).

## 5. Technology Viewpoint (Ponto de Vista de Tecnologia)
**Restrições:** AWS Academy Learner Lab (Sem Glue, Sem Redshift).
- **Armazenamento de Origem:** Amazon S3.
- **Fila de Eventos:** Amazon SQS.
- **Orquestração:** AWS Step Functions.
- **Computação:** AWS ECS Fargate (Docker).
- **Banco de Dados:** Amazon RDS Postgres (Single-AZ p/ Lab).
- **Monitoramento:** AWS CloudWatch + X-Ray + Grafana (Externo/Sidecar).

---

## 🏗️ Architecture Decision Records (ADRs)

### ADR 001: Uso de RDS Postgres em vez de Redshift
- **Contexto:** Necessidade de um repositório persistente com suporte a transações ACID e lógica de UPSERT, operando dentro dos limites do AWS Academy Learner Lab.
- **Decisão:** Utilizar Amazon RDS com engine Postgres.
- **Consequências:** Atendimento ao RF-04 e RNF-08. Limitação de escalabilidade analítica extrema compensada pelo baixo custo e facilidade de manutenção no ambiente de lab.

### ADR 002: AWS ECS Fargate para Processamento de Lote
- **Contexto:** O processamento de 100k registros pode exceder os 15 minutos do AWS Lambda e o AWS Glue não está disponível no lab.
- **Decisão:** Utilizar containers Docker rodando no AWS ECS Fargate.
- **Consequências:** Atendimento ao RNF-02 e RNF-10. Permite execução de longa duração, controle total do ambiente de execução e escalabilidade horizontal.

### ADR 003: Idempotência via Staging + SQL ON CONFLICT
- **Contexto:** Garantir que reprocessamentos não causem duplicidade (RF-04) sem complexidade excessiva de código.
- **Decisão:** Carregar dados brutos em uma tabela de `staging` e usar o comando `INSERT ... ON CONFLICT` do Postgres para mover para a produção.
- **Consequências:** Atendimento ao RF-04 e RNF-01. Simplicidade na recuperação de falhas e garantia de integridade a nível de banco de dados.

---
**Nota:** Este documento mapeia os componentes aos requisitos definidos em `01_functional_requirements.md` e `02_non_functional_requirements.md`.
