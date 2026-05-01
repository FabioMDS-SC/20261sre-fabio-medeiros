# Skill: Elicitação de Requisitos Não Funcionais (RNF)

Esta habilidade orienta o agente na definição de requisitos de qualidade técnica baseados na norma ISO 25010, garantindo que o sistema seja robusto, escalável e operável.

## 🎯 Quando usar
Use esta skill quando for solicitado o levantamento de RNFs e já existirem os arquivos `specs/00_problem.md` e/ou `documents/01_functional_requirements.md`.

## 📥 Entrada
- `specs/00_problem.md` (Obrigatório)
- `documents/01_functional_requirements.md` (Opcional, mas recomendado)

## 🛠️ Metodologia (Passos)

1.  **Análise de Contexto:** Ler stakeholders e fluxos críticos no documento de problema.
2.  **Mapeamento ISO 25010:** Mapear cada fluxo crítico aos 8 atributos de qualidade:
    - Adequação Funcional
    - Eficiência de Desempenho
    - Compatibilidade
    - Usabilidade
    - Confiabilidade
    - Segurança
    - Manutenibilidade
    - Portabilidade
3.  **Definição de Métricas:** Para cada atributo, propor 1 a 3 RNFs com SLIs (Service Level Indicators) mensuráveis.
4.  **Priorização:** Aplicar técnica MoSCoW.
5.  **Fontes e Janelas:** Listar premissas e onde a medição será realizada (ex: CloudWatch, X-Ray).

## 📝 Formato de Saída (`documents/02_non_functional_requirements.md`)

O documento final deve conter:
- Seções individuais por atributo ISO 25010.
- IDs únicos no formato `RNF-NN`.
- Uma **Tabela de Resumo** final contendo:
    | ID | Atributo | SLI (Métrica) | SLO (Meta) | Fonte de Medição | Prioridade |
    | :--- | :--- | :--- | :--- | :--- | :--- |

## 🤖 Instruções para o Agente
- **Proibição de Termos Aspiracionais:** Nunca use termos vagos como "o sistema deve ser rápido" ou "deve ser confiável". Substitua por métricas exatas (ex: "tempo de resposta < 2s").
- **Janela de Medição:** Todo RNF deve ter uma unidade de medida e uma janela temporal (ex: "99.9% de sucesso em uma janela de 30 dias").
- **Alinhamento Técnico:** Garanta que os SLOs propostos sejam viáveis dentro da stack tecnológica definida no projeto (AWS).

## 📋 Critérios de Aceitação da Skill
- [ ] Todos os 8 atributos da ISO 25010 foram endereçados.
- [ ] Cada RNF possui um SLI técnico e mensurável.
- [ ] A tabela resumo está completa e consistente com o texto.
- [ ] As janelas de observação estão definidas.
