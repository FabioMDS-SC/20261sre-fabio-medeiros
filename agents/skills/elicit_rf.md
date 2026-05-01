# Skill: Elicitação de Requisitos Funcionais (RF)

Esta habilidade orienta o agente na identificação, documentação e validação das funcionalidades que o sistema deve executar para atender aos objetivos de negócio.

## 🎯 Objetivo
Garantir que todos os requisitos funcionais sejam capturados de forma clara, sem ambiguidades, e que estejam diretamente ligados à necessidade de modernização do pipeline de dados da Olist.

## 🛠️ Metodologia de Elicitação

1.  **Identificação de Atores:** Quem ou o que interage com o sistema (ex: Operadores de Dados, AWS S3, RDS).
2.  **Definição de Escopo:** O que o sistema *deve* e *não deve* fazer.
3.  **Processo Iterativo:**
    *   **Descoberta:** Questionar o propósito de cada funcionalidade.
    *   **Classificação:** Agrupar requisitos por módulo (Ingestão, Transformação, Carga, Monitoramento).
    *   **Priorização:** Utilizar técnica MoSCoW (Must-have, Should-have, Could-have, Won't-have).
    *   **Validação:** Verificar se o requisito é testável e necessário.

## 📝 Diretrizes de Escrita (SMART)
Cada requisito funcional deve ser:
-   **Específico:** Descrever uma única funcionalidade.
-   **Mensurável:** Deve ser possível verificar se foi implementado.
-   **Alcançável:** Tecnicamente viável na stack AWS proposta.
-   **Relevante:** Deve agregar valor ao pipeline de pedidos.
-   **Temporal:** Ter um contexto de quando ocorre no workflow.

## 🤖 Instruções para o Agente
Ao atuar com esta skill:
1.  Sempre sugira requisitos implícitos baseados em boas práticas de engenharia de dados (ex: logs de auditoria, tratamento de arquivos corrompidos).
2.  Formate os requisitos seguindo o padrão: `RFXX: [Título] - [Descrição detalhada]`.
3.  Garanta a rastreabilidade inicial para a Matriz de Rastreabilidade (RTM).
4.  Ao editar o arquivo `documents/01_functional_requirements.md`, mantenha a consistência com os requisitos já existentes.

## 📋 Checklist de Qualidade
- [ ] O requisito descreve *o que* o sistema faz, não *como* ele faz?
- [ ] Existe alguma contradição com outros RFs ou RNFs?
- [ ] O requisito é atômico?
- [ ] O critério de aceitação está claro?
