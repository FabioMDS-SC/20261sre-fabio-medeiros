# 08. System Design (Detalhamento do Sistema)

Este documento detalha o design técnico dos componentes da arquitetura local OLAP, focando na integração via Docker e no fluxo de dados.

## 1. Arquitetura de Containers (Docker Compose)

O sistema é composto pelos seguintes serviços integrados em uma rede Docker interna:

- **`minio`**: Servidor de Object Storage local para armazenamento dos arquivos CSV (Bronze).
- **`clickhouse`**: Banco de Dados OLAP para armazenamento analítico (Silver/Gold).
- **`ingestion-engine`**: Container Python/DuckDB que realiza o movimento de dados do MinIO para o ClickHouse.
- **`dbt-runner`**: Container responsável por executar as transformações SQL dentro do ClickHouse.
- **`streamlit`**: Interface de dashboard para visualização dos dados.

## 2. Procedimento de Carga de Dados (Manual/CLI)

Caso a interface gráfica do MinIO não esteja acessível, o upload de arquivos pode ser realizado via container do MinIO Client (`mc`):

```bash
docker run --rm -v ./dados_olist:/data --network olist_network \
  --entrypoint /bin/sh minio/mc \
  -c "mc alias set myminio http://minio:9000 admin password123 && mc cp /data/ myminio/olist-raw/ --recursive"
```

Este comando:
1. Mapeia a pasta local `./dados_olist` para o container.
2. Configura o alias para o servidor MinIO interno.
3. Copia recursivamente todos os CSVs para o bucket `olist-raw`.

## 3. Fluxo de Dados (Step-by-Step)

1.  **Landing Zone**: O operador ou processo externo coloca os arquivos CSV no bucket `olist-raw` do MinIO.
2.  **Ingestion**: O `ingestion-engine` detecta os arquivos, utiliza o **DuckDB** para ler o S3 local de forma eficiente e faz o stream dos dados para a tabela `staging` no **ClickHouse**.
3.  **Storage**: O ClickHouse persiste os dados utilizando o engine `MergeTree`, garantindo alta compressão e velocidade de leitura.
4.  **Transformation**: O `dbt-runner` executa modelos SQL que criam visões de negócio na camada Gold do ClickHouse:
    - `stg_orders`: Limpeza e tipagem dos dados de pedidos.
    - `stg_order_items`: Processamento de itens e valores.
    - `fct_orders`: Tabela fato consolidada com KPIs de vendas (GMV, ticket médio).
5.  **Visualization**: O Streamlit consulta a tabela `fct_orders` para exibir:
    - KPIs em tempo real (GMV, Pedidos, Clientes).
    - Tendências de vendas diárias.
    - Distribuição de status de pedidos.

## 3. Estratégia de Performance

- **DuckDB as a Middleware**: Utilizado na ingestão por sua capacidade nativa de ler CSVs e S3 de forma extremamente rápida, servindo como um "motor de movimentação" leve.
- **Columnar Storage**: O ClickHouse armazena os dados em colunas, permitindo que o dashboard leia apenas os campos necessários (ex: data e valor) sem ler o registro inteiro.

## 4. Gerenciamento de Configuração

- **Variáveis de Ambiente**: Todas as credenciais de acesso (MinIO keys, ClickHouse users) são gerenciadas via arquivo `.env`.
- **Volumes Persistentes**: Docker volumes são utilizados para garantir que os dados do MinIO e ClickHouse não sejam perdidos ao reiniciar os containers.
