# 🏗️ Architecture Review: Len Bass Tactics

Este documento detalha a revisão da arquitetura do projeto **Olist Data Pipeline** baseada nas táticas arquiteturais de **Len Bass** (Software Architecture in Practice).

## 1. Avaliação de Táticas por Atributo de Qualidade

### 1.1 Disponibilidade (Availability)
*   **Tática Ping/Echo:** ✅ Implementada via healthchecks no Docker Compose.
*   **Tática Exception Handling:** ⚠️ Parcial no `ingest.py`. O sistema encerra sem logs estruturados em falhas críticas de I/O.
*   **Tática Retry:** ❌ Ausente. Falhas transitórias de rede causam interrupção definitiva do pipeline.
*   **Idempotência:** ⚠️ Não garantida. Reexecução de arquivos gera duplicação de linhas no ClickHouse.

### 1.2 Performance
*   **Tática Cache:** 🟡 Implementada na conexão, mas ausente nos resultados de queries pesadas no Streamlit.
*   **Tática Bulkhead:** ✅ Implementada através do isolamento de containers Docker.
*   **Tática Timeouts:** ❌ Não configurados explicitamente nas bibliotecas de conexão.

### 1.3 Segurança (Security)
*   **Limit Exposure:** ✅ Redes isoladas e gestão de segredos via `.env`.
*   **Authenticate Actors:** ✅ Autenticação ativa em todos os serviços (MinIO, ClickHouse).

### 1.4 Testabilidade (Testability)
*   **Componentes de Teste:** ⚠️ Ausentes no código atual (Python/Streamlit).
*   **QA Pipeline:** 💎 **Destaque:** O framework `aiox qa` já fornece a infraestrutura para executar os portões de qualidade, mas falta a implementação dos testes específicos.

---

## 2. Roadmap de Evolução (Waves de Mudança) - STATUS: CONCLUÍDO ✅

### 🌊 Wave 1: Estabilização e Resiliência (Disponibilidade) - [CONCLUÍDO]
*   **Implementação de Retry:** ✅ Adicionada biblioteca `tenacity` com backoff exponencial nas funções de leitura e escrita.
*   **Idempotência de Ingestão:** ✅ Implementada verificação via `SELECT count()` por `tag` antes de novos inserts.
*   **Timeouts Explícitos:** ✅ Configurados timeouts de conexão e leitura para Boto3 (5s/10s) e ClickHouse (10s).

### 🌊 Wave 2: Eficiência e UX (Performance) - [CONCLUÍDO]
*   **Query Caching:** ✅ Implementado `@st.cache_data` com TTL dinâmico (300s-600s) para métricas e status no Streamlit.
*   **Isolamento Bulkhead:** ✅ Validado via arquitetura de containers Docker.

### 🌊 Wave 3: Maturidade e Observabilidade (Operações) - [CONCLUÍDO]
*   **Circuit Breaker:** ✅ Implementado contador de falhas consecutivas (limite: 3) para interromper o pipeline em falhas críticas.
*   **Logs Estruturados:** ✅ Migração de `print` para logs JSON estruturados via Python `logging`.
*   **DLQ (Dead Letter Queue):** ✅ Arquivos com erro são automaticamente movidos para o prefixo `olist-failed/` no MinIO.

### 🌊 Wave 4: Qualidade e Governança (Testabilidade) - [CONCLUÍDO]
*   **Testes Unitários:** ✅ Suíte de testes criada em `ingestion/test_ingest.py` usando `pytest` e `mocker`.
*   **Cobertura:** ✅ Validadas funções de idempotência, leitura do S3, escrita no ClickHouse e conversão JSON.


---

## 3. Matriz de Sensibilidade (ATAM)

| ID | Ponto de Sensibilidade | Tática Recomendada | Impacto |
| :--- | :--- | :--- | :--- |
| **SP-01** | Duplicação de dados | Idempotency | Integridade dos Dados |
| **SP-02** | Instabilidade de Rede | Retry / Backoff | Continuidade do Negócio |
| **SP-03** | Latência do Dashboard | Cache | Satisfação do Usuário |
| **SP-04** | Processos Travados | Timeouts | Gestão de Recursos |

---
*Documento gerado automaticamente pela revisão de arquitetura AIOX/Gemini.*
