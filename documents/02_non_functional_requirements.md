# 02. Requisitos Não Funcionais (RNF)

Este documento define os requisitos de qualidade técnica para o pipeline de processamento de pedidos, estruturados de acordo com a norma ISO 25010 e focados em métricas mensuráveis (SLI/SLO).

## 1. Adequação Funcional (Functional Suitability)
- **RNF-01: Completude do Processamento**
    - **Descrição:** Garantir que todos os registros válidos identificados no arquivo de origem sejam persistidos no repositório final.
    - **SLI:** Razão entre registros persistidos e registros válidos na origem.
    - **SLO:** 100% de sucesso por lote de processamento.
    - **Prioridade:** Must-have

## 2. Eficiência de Desempenho (Performance Efficiency)
- **RNF-02: Vazão de Processamento (Throughput)**
    - **Descrição:** O sistema deve ser capaz de processar a carga diária de 100 mil pedidos dentro de uma janela operacional aceitável.
    - **SLI:** Tempo total de processamento do lote diário.
    - **SLO:** < 4 horas para 100k registros.
    - **Prioridade:** Must-have

- **RNF-03: Latência de Ingestão (Data Freshness)**
    - **Descrição:** Tempo máximo para que um registro disponível na origem apareça no repositório persistente.
    - **SLI:** Tempo decorrido do evento de detecção até o commit no banco final.
    - **SLO:** < 15 minutos (P95).
    - **Prioridade:** Should-have

## 3. Compatibilidade (Compatibility)
- **RNF-04: Interoperabilidade de Formatos**
    - **Descrição:** O serviço de processamento deve ser capaz de ler arquivos de texto delimitados independentemente da codificação (UTF-8/ISO-8859-1).
    - **SLI:** Taxa de sucesso na leitura de arquivos com diferentes encodings.
    - **SLO:** 100% de sucesso para encodings homologados.
    - **Prioridade:** Should-have

## 4. Usabilidade (Usability)
- **RNF-05: Operabilidade de Alertas**
    - **Descrição:** Alertas críticos devem conter contexto suficiente para ação imediata sem necessidade de busca manual profunda em logs.
    - **SLI:** Tempo médio para diagnóstico inicial (MTTD).
    - **SLO:** < 5 minutos para falhas críticas.
    - **Prioridade:** Must-have

## 5. Confiabilidade (Reliability)
- **RNF-06: Taxa de Sucesso do Pipeline (Availability)**
    - **Descrição:** Disponibilidade do pipeline para processar novos dados assim que disponibilizados.
    - **SLI:** % de execuções finalizadas com sucesso sem intervenção manual.
    - **SLO:** 99.9% (Janela mensal).
    - **Prioridade:** Must-have

- **RNF-07: Recuperabilidade (Recoverability)**
    - **Descrição:** Capacidade de reiniciar o processamento a partir de falhas parciais (ex: falha de rede) sem perda de dados ou duplicação.
    - **SLI:** Tempo de recuperação automática após falha transitória.
    - **SLO:** < 10 minutos para retentativa automática.
    - **Prioridade:** Must-have

## 6. Segurança (Security)
- **RNF-08: Proteção de Dados em Repouso**
    - **Descrição:** Todos os dados armazenados nas áreas de estágio e persistência devem ser protegidos contra acesso não autorizado e corrupção.
    - **SLI:** Auditoria de conformidade de criptografia e permissões.
    - **SLO:** 100% dos volumes/buckets criptografados.
    - **Prioridade:** Must-have

## 7. Manutenibilidade (Maintainability)
- **RNF-09: Observabilidade Distribuída**
    - **Descrição:** Capacidade de rastrear uma unidade de processamento através de todos os componentes do sistema.
    - **SLI:** % de execuções com Trace ID único persistido e correlacionado.
    - **SLO:** 100%.
    - **Prioridade:** Should-have

## 8. Portabilidade (Portability)
- **RNF-10: Independência de Ambiente**
    - **Descrição:** O componente de processamento deve ser executável em ambientes de container padronizados.
    - **SLI:** Tempo de setup de um novo ambiente de execução via IaC/Container.
    - **SLO:** < 30 minutos.
    - **Prioridade:** Could-have

---

## Tabela de Resumo de Requisitos Não Funcionais

| ID | Atributo | SLI (Métrica) | SLO (Meta) | Fonte de Medição | Prioridade |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RNF-01 | Adequação Funcional | Razão Registros Origem/Destino | 100% | Auditoria de Logs | Must-have |
| RNF-02 | Performance | Tempo de Lote (100k) | < 4 horas | Monitoramento de Workflow | Must-have |
| RNF-03 | Performance | Data Freshness (P95) | < 15 min | Logs de Timestamp | Should-have |
| RNF-04 | Compatibilidade | Sucesso de Encoding | 100% | Logs de Validação | Should-have |
| RNF-05 | Usabilidade | Tempo de Diagnóstico (MTTD) | < 5 min | Painel de Incidentes | Must-have |
| RNF-06 | Confiabilidade | Pipeline Success Rate | 99.9% | Métrica de Orquestração | Must-have |
| RNF-07 | Confiabilidade | Tempo de Recuperação | < 10 min | Logs de Retry | Must-have |
| RNF-08 | Segurança | Taxa de Criptografia | 100% | Cloud Auditor | Must-have |
| RNF-09 | Manutenibilidade | Cobertura de Tracing | 100% | Sistema de Tracing | Should-have |
| RNF-10 | Portabilidade | Tempo de Provisionamento | < 30 min | Logs de Deploy/CI | Could-have |

---
**Nota:** Este documento segue as diretrizes da skill `agents/skills/elicit_rnf.md` e a norma ISO 25010.
