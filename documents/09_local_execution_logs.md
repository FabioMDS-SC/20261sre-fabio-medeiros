# 09. Local Execution Logs (Registro de Execução Local)

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
