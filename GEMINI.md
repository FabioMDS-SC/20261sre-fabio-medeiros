# GEMINI.md

## Projeto: Modernização do Pipeline de Ingestão de Dados (Olist)

Este projeto tem como objetivo a estabilização e modernização do pipeline de ingestão de dados da Olist, processando arquivos CSV do Amazon S3 para o Amazon RDS Postgres. A arquitetura é orientada a eventos, utilizando serviços AWS para garantir escalabilidade e resiliência.

## 📂 Estrutura de Diretórios

O projeto está organizado para suportar tanto a documentação técnica quanto a automação via agentes de IA.

### 📄 `documents/` (Documentação do Projeto)
Este diretório contém toda a documentação oficial do ciclo de vida do software.
- `00_index.md`: Ponto de entrada e índice de toda a documentação.
- `01_functional_requirements.md`: Definição detalhada dos Requisitos Funcionais (RF).
- `02_non_functional_requirements.md`: Requisitos Não Funcionais (RNF) baseados no SWEBOK.
- `03_architecture.md`: Descrição da arquitetura proposta e diagramas.
- `04_rtm.md`: Matriz de Rastreabilidade de Requisitos (RTM).
- `05_test_plan_load.md`: Plano de testes de carga e desempenho.
- `06_test_plan_security.md`: Plano de testes de segurança e conformidade.
- `07_test_plan_modeling.md`: Modelagem de dados e testes de integridade.
- `08_system_design.md`: Detalhes de design do sistema e componentes.
- `09_aws_cli_session.md`: Registro de comandos e sessões AWS CLI.

### 🤖 `agents/` (Framework de Agentes)
Contexto e definições para agentes de IA que auxiliam no desenvolvimento.
- `AGENTS.md`: Definição dos papéis e responsabilidades dos agentes.
- `GEMINI.md`: Instruções específicas para o modelo Gemini neste contexto.
- **`skills/`**: Habilidades especializadas para automação:
  - `elicit_rf.md` / `elicit_rnf.md`: Auxílio na elicitação de requisitos.
  - `build_rtm.md`: Automação da construção da matriz de rastreabilidade.
  - `review_architecture.md`: Revisão técnica de arquitetura.
  - `plan_load_test.md` / `plan_security_test.md`: Planejamento de testes.

### 📝 `specs/`
- `00_problem.md`: Definição original do problema e contexto de negócio.

## 🛠️ Fluxo de Uso
1. **Requisitos:** Iniciar pela elicitação em `documents/01` e `02`.
2. **Arquitetura:** Definir o design em `documents/03` e `08`.
3. **Rastreabilidade:** Manter a `04_rtm.md` atualizada conforme os requisitos evoluem.
4. **Validação:** Seguir os planos de teste em `documents/05`, `06` e `07`.

## 🏗️ Tecnologias Principais (Inferidas)
- **Cloud:** AWS (S3, RDS, Lambda, ECS, Step Functions).
- **IaC:** Terraform/CloudFormation (Planejado).
- **Monitoramento:** CloudWatch, X-Ray, Grafana.
