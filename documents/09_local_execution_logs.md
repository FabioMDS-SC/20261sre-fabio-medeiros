# 09. Registro de Execução Local

## Sessão: 18/05/2026

### Atividades Realizadas
1. **Inicialização do Ambiente:**
   - Comando: `docker-compose up -d`
   - Resultado: Todos os serviços (MinIO, ClickHouse, Ingestion, dbt-runner, Streamlit) iniciados com sucesso.
   - Verificação: ClickHouse saudável e dados persistidos em volumes carregados.

2. **Teste de Carga (Non-Functional):**
   - Ferramenta: `k6` via Docker.
   - Script: `tests/load_test.js` (atualizado com credenciais corretas: `default`/`password123`).
   - Resultado: **Sucesso**. p(95) de 36.26ms, atendendo ao SLO de < 1s.

3. **Verificação de Integridade de Dados:**
   - Adição de testes dbt (`schema.yml`) para o modelo `fct_orders`.
   - Execução: `dbt test` no container `dbt-runner`.
   - Resultado: **4/4 testes aprovados** (Unique e Not Null).

4. **Auditoria de Pipeline:**
   - Verificado logs do `ingestion-engine`.
   - Confirmado que o mecanismo de idempotência está funcionando (pulando arquivos já processados).

### Métricas Observadas
- **Tempo de Inicialização:** ~1 minuto.
- **RPS (Consultas Analíticas):** ~15 req/s.
- **Volume de Dados:** ~1.6M de registros processados na camada de ingestão.

### Próximos Passos
- Explorar o dashboard Streamlit em `http://localhost:8501`.
- Expandir os modelos dbt para incluir mais métricas de negócio.
