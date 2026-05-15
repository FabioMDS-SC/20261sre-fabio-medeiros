# 09. Local Execution Logs (Registro de Execução Local)

## Sessão 2026-05-15: Substituição do Grafana pelo Streamlit

### Decisão
Substituir o Grafana pelo Streamlit para maior flexibilidade no desenvolvimento de dashboards e KPIs personalizados usando Python, facilitando a integração com a stack de dados atual.

### Ações Realizadas
1.  **Infraestrutura**:
    - Removido o serviço `grafana` do `docker-compose.yml`.
    - Adicionado o serviço `streamlit` configurado para rodar na porta `8501`.
    - Criado o diretório `dashboard/` contendo `app.py` (código do dashboard) e `requirements.txt`.
2.  **Estabilização da Ingestão**:
    - Corrigido o nome do script no `docker-compose.yml` de `ingestion.py` para `ingest.py`.
    - Atualizado `ingest.py` para criar o bucket `olist-raw` automaticamente.
    - Ajustado o `healthcheck` do ClickHouse para evitar falhas de dependência na inicialização.
3.  **Carga de Dados**:
    - Realizado o upload de 9 arquivos CSV via MinIO Client (`mc`) devido a dificuldades de acesso ao console web.
    - Confirmada a ingestão de >1.6M de registros no ClickHouse.
4.  **Transformação (dbt)**:
    - Inicializado projeto dbt em `dbt/`.
    - Implementados modelos de staging (`stg_orders`, `stg_order_items`) e fato (`fct_orders`).
    - Configurado `profiles.yml` para conectividade com ClickHouse via `dbt-runner`.
5.  **Dashboard de Negócio**:
    - Evoluído `dashboard/app.py` com métricas analíticas (GMV, Ticket Médio, Tendências).
    - Adicionada integração com Plotly para visualizações dinâmicas.
6.  **Documentação**:
    - Atualizados todos os documentos (`01_functional_requirements.md`, `02_non_functional_requirements.md`, `03_architecture.md`, `08_system_design.md`, `GEMINI.md`) substituindo referências ao Grafana por Streamlit e detalhando a camada dbt.
7.  **Cleanup**:
    - Removidos arquivos e pastas de provisionamento do Grafana em `ingestion/`.

---
## Sessão 2026-05-09: Investigação de Erros no Docker Compose

### Problema Relatado
O usuário tentou subir o ambiente Docker em seu computador pessoal e encontrou "diversos erros".

### Investigação
1.  **Configuração de Redirect do MinIO**: Identificamos que a variável `MINIO_BROWSER_REDIRECT_URL` no `docker-compose.yml` estava "hardcoded" para o formato do GitHub Codespaces, o que impede o acesso correto à console do MinIO em ambiente local (localhost).
2.  **Variáveis de Ambiente**: As variáveis `${CODESPACE_NAME}` e `${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}` não estão definidas em ambientes locais, gerando avisos ou URLs inválidas.
3.  **Logs do Grafana**: Observamos um erro de permissão ao tentar atualizar o plugin do Elasticsearch (`permission denied`). Este erro parece ser relacionado à tentativa do Grafana de modificar arquivos dentro da imagem (bundled plugins), o que geralmente não impede o funcionamento básico do serviço.

### Ações Realizadas
1.  **Mudança de Porta do Console**: Alterada a porta externa do console do MinIO de `9001` para `9090` no `docker-compose.yml`. Isso resolve possíveis conflitos com processos locais e evita problemas de redirecionamento residual do Codespaces.
2.  **Limpeza do `docker-compose.yml`**: Removida completamente a variável `MINIO_BROWSER_REDIRECT_URL`.

### Próximos Passos
- Validar acesso via porta 9090 em aba anônima.
