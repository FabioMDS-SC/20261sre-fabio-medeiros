# 01. Requisitos Funcionais (RF)

Este documento detalha as funcionalidades necessárias para a modernização do pipeline de ingestão de dados, garantindo que o sistema atenda aos objetivos de negócio e operacionais de forma independente da tecnologia de infraestrutura.

## 👥 Atores do Sistema
- **Sistema de Origem de Dados:** Entidade externa que fornece os arquivos de entrada (ex: armazenamento de objetos ou sistema de arquivos).
- **Serviço de Processamento:** Componente responsável pela execução da lógica de negócio, validação e transformação dos dados.
- **Repositório de Dados Persistentes:** Destino final onde os dados processados são armazenados para consumo analítico e operacional.
- **Operador de Sistema:** Usuário responsável pelo monitoramento da saúde do pipeline e intervenção em caso de falhas.

## 🛠️ Requisitos de Ingestão e Processamento

### RF01: Detecção Automática de Novos Dados
- **Descrição:** O sistema deve detectar automaticamente a disponibilidade de novos conjuntos de dados no formato de arquivo de texto delimitado (ex: CSV) e iniciar o fluxo de processamento sem intervenção manual.
- **Prioridade:** Must-have
- **Critério de Aceitação:** A detecção e o início do processamento devem ocorrer em até 30 segundos após a disponibilização do dado na origem.

### RF02: Validação de Estrutura e Tipagem
- **Descrição:** O sistema deve validar se os dados de entrada seguem o esquema definido, incluindo a presença de campos obrigatórios, tipos de dados corretos e restrições de formato.
- **Prioridade:** Must-have
- **Critério de Aceitação:** Registros que não atendam ao esquema devem ser isolados em uma área de quarentena, e o evento deve ser registrado para posterior análise.

### RF03: Estágio Intermediário de Dados
- **Descrição:** O sistema deve permitir o carregamento dos dados validados em uma área de estágio temporária para possibilitar operações de limpeza, deduplicação e validações cruzadas.
- **Prioridade:** Should-have
- **Critério de Aceitação:** Todos os registros válidos do arquivo devem ser acessíveis na área de estágio antes da persistência definitiva.

### RF04: Persistência com Garantia de Idempotência (UPSERT)
- **Descrição:** O sistema deve persistir os dados no repositório final garantindo que registros novos sejam inseridos e registros existentes sejam atualizados (UPSERT), evitando duplicidade em caso de reprocessamento.
- **Prioridade:** Must-have
- **Critério de Aceitação:** O reprocessamento de um mesmo conjunto de dados não deve gerar registros duplicados no repositório de dados persistentes.

## 📊 Requisitos de Observabilidade e Auditoria

### RF05: Rastreabilidade e Auditoria de Execução
- **Descrição:** O sistema deve registrar o histórico de cada execução, incluindo metadados como: identificador do conjunto de dados, horários de início e fim, contagem de registros processados e status da operação.
- **Prioridade:** Must-have
- **Critério de Aceitação:** O histórico deve ser consultável por ferramentas de monitoramento e auditoria.

### RF06: Notificação de Eventos Críticos
- **Descrição:** O sistema deve emitir alertas automáticos aos operadores quando ocorrerem falhas que impeçam a conclusão bem-sucedida do pipeline ou violações de integridade.
- **Prioridade:** Must-have
- **Critério de Aceitação:** O alerta deve ser gerado e entregue aos canais de comunicação definidos em até 2 minutos após a detecção da anomalia.

### RF07: Disponibilização de Métricas de Throughput
- **Descrição:** O sistema deve exportar métricas operacionais relacionadas ao volume de dados processados por unidade de tempo para visualização em dashboards.
- **Prioridade:** Should-have
- **Critério de Aceitação:** As métricas devem refletir o estado do processamento com uma latência máxima de 5 minutos.

---
**Nota:** Este documento foi refatorado para ser agnóstico à ferramenta, seguindo as diretrizes da skill `agents/skills/elicit_rf.md`.
