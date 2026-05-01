# Problema: Processamento de Pedidos Olist

## Contexto do Negócio
O negócio Olist precisa processar aproximadamente **100 mil pedidos** do marketplace diariamente, carregá-los em um banco analítico (Postgres) e gerar dashboards para tomada de decisão. 

### Requisitos Mandatórios do ETL
- **Confiabilidade:** O processo deve ser robusto e previsível.
- **Idempotência:** Garantir que reprocessar o mesmo dado não gere duplicidade.
- **Observabilidade:** Capacidade de monitorar o progresso e saúde do pipeline.
- **Resiliência:** Capacidade de recuperar-se de falhas parciais sem intervenção manual exaustiva.
- **Integridade:** Não podemos perder dados, duplicá-los ou sofrer falhas silenciosas.

---

## Canvas de Modelagem do Problema

### 1. Stakeholders
- **Operação Olist (Negócio):** Donos do processo que dependem da acurácia para operar.
- **Time de Dados:** Responsáveis técnicos pelo pipeline de ETL.
- **Clientes Internos do Dashboard:** Usuários finais que consomem as métricas.
- **Plataforma / SRE:** Responsáveis pela infraestrutura, estabilidade e custos.

### 2. Fluxos Críticos
- **Ingestão Diária:** Extração do CSV e carga no Postgres.
- **Consulta de Dashboards:** Disponibilização dos dados via Grafana para os usuários.
- **Observação de SLA:** Monitoramento contínuo para garantir que o dado esteja disponível no tempo acordado.

### 3. Modos de Falha
- **Arquivo corrompido ou parcial:** Origem de dados inconsistente.
- **Reprocesso duplicando linhas:** Falha na lógica de carga que ignora dados já existentes.
- **Queda de instância (EC2) durante o run:** Interrupção do processamento por falha de hardware ou infra.
- **Banco de dados indisponível:** Postgres fora do ar ou recusando conexões.

### 4. Riscos Sistêmicos
- **Perda silenciosa de linhas:** O pipeline termina sem erros, mas com dados faltando (o risco mais crítico).
- **Dashboard mostrando dado stale (obsoleto):** Usuário toma decisão baseada em dados de ontem sem saber.
- **Custo AWS explodindo:** Má gestão de recursos de infraestrutura levando a cobranças inesperadas.
- **Dívida técnica de IA mal revisada:** Implementações automatizadas sem a devida governança ou revisão de código.
