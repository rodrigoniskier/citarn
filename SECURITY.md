# Segurança do CitaRN

## Antes da produção

- Use `DEBUG=False` e uma `SECRET_KEY` exclusiva e aleatória.
- Restrinja `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` ao domínio real.
- Ative HTTPS, cookies seguros e HSTS.
- Proteja a conta do PythonAnywhere e a conta do GitHub com autenticação em dois fatores.
- Mantenha `.env`, banco, uploads e backups fora do Git.
- Execute `python manage.py check --deploy` após cada mudança de configuração.

## Arquivos enviados

O aplicativo limita extensão, quantidade e tamanho dos uploads e nunca executa o conteúdo enviado. Arquivos ficam fora da árvore estática e são baixados por uma visão autenticada com verificação de proprietário.

Para uso institucional, recomenda-se acrescentar varredura antivírus antes do armazenamento definitivo. Essa camada não está incluída na versão inicial por exigir um serviço ou processo adicional.

## URLs e SSRF

Antes de buscar uma URL, o sistema aceita apenas HTTP/HTTPS, rejeita credenciais incorporadas e bloqueia endereços locais, privados, reservados e não roteáveis. Redirecionamentos são revalidados e o tamanho máximo da resposta é limitado.

## Privacidade

Todas as consultas de projeto, referência e arquivo filtram o usuário autenticado. O painel administrativo deve ser concedido apenas a responsáveis autorizados.

## Incidentes

Em caso de suspeita de exposição:

1. retire o aplicativo do ar;
2. troque a `SECRET_KEY`, senhas administrativas e credenciais do banco;
3. preserve os logs para análise;
4. verifique usuários, permissões e arquivos;
5. restaure apenas um backup íntegro;
6. avalie as obrigações de comunicação previstas na LGPD.
