# Plano de Teste de Carga - Resultados

## 1. Objetivo
Avaliar a performance do ClickHouse ao processar consultas analíticas complexas sob carga simulada de múltiplos usuários.

## 2. Cenário de Teste
- **Script:** `tests/load_test.js`
- **Query:** `SELECT order_status, count() as orders, sum(total_order_value) as gmv FROM olist.fct_orders GROUP BY order_status`
- **Configuração:**
  - Estágio 1: Rampa de subida (10s) até 20 VUs (Usuários Virtuais).
  - Estágio 2: Manutenção (20s) com 20 VUs.
  - Estágio 3: Rampa de descida (10s) até 0 VUs.
- **Sleep:** 1 segundo entre iterações por usuário.

## 3. Resultados (Execução em 18/05/2026)

| Métrica | Valor |
|---------|-------|
| **Total de Requisições** | 610 |
| **Taxa de Sucesso (Status 200)** | 100% |
| **Duração Média (http_req_duration)** | 13.56ms |
| **Duração p(95)** | 36.26ms |
| **Duração Máxima** | 79.96ms |
| **Requisições por Segundo (RPS)** | ~15.08 req/s |

## 4. Conclusão
O sistema atendeu ao requisito de performance (RNF) com folga significativa. O limite estabelecido era de `p(95) < 1000ms`, e o resultado obtido foi de **36.26ms**. 
O ClickHouse demonstrou excelente eficiência para a volumetria atual (99.441 linhas na tabela `fct_orders`).

## 5. Próximos Passos
- Realizar testes de estresse com volume de dados 10x maior.
- Validar concorrência com 100+ VUs.
