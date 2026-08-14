# Deploy do CitaRN no PythonAnywhere

Este roteiro segue o fluxo oficial do PythonAnywhere para projetos Django existentes: clonar o repositório, criar um ambiente virtual, usar a configuração web manual, apontar o WSGI e configurar arquivos estáticos.

Documentação oficial consultada:

- <https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/>
- <https://help.pythonanywhere.com/pages/UsingMySQL/>
- <https://help.pythonanywhere.com/pages/FreeAccountsFeatures/>
- <https://www.pythonanywhere.com/whitelist/>

## 1. Decisão de banco

Para a primeira implantação, use **SQLite**. Ele é persistente no PythonAnywhere e suficiente para uso individual ou um grupo pequeno, desde que os uploads e gravações concorrentes sejam moderados.

Em agosto de 2026, contas gratuitas novas oferecem 512 MiB, um aplicativo web e um único worker; MySQL gratuito permanece disponível apenas para algumas contas antigas. Por isso, o CitaRN usa SQLite por padrão e não pressupõe acesso a MySQL.

Se a quantidade de usuários ou gravações simultâneas crescer, migre para MySQL em um plano compatível. Não é necessário alterar os modelos ou as telas.

## 2. Clonar o repositório

Abra um **Bash Console** no PythonAnywhere:

```bash
cd ~
git clone https://github.com/SEU-USUARIO/citarn.git
cd citarn
```

Para repositório privado, use uma chave SSH ou um token seguindo as orientações do GitHub; nunca grave o token dentro do repositório.

## 3. Criar o ambiente virtual

Escolha na interface Web a mesma versão de Python usada no ambiente virtual. O exemplo abaixo usa Python 3.12; ajuste se a sua conta oferecer outra versão:

```bash
mkvirtualenv --python=/usr/bin/python3.12 citarn-venv
workon citarn-venv
pip install -r ~/citarn/requirements.txt
```

## 4. Criar o arquivo de configuração privado

```bash
cd ~/citarn
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Edite `~/citarn/.env` e use a chave exibida:

```dotenv
SECRET_KEY=COLE-A-CHAVE-GERADA
DEBUG=False
ALLOWED_HOSTS=SEUUSUARIO.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://SEUUSUARIO.pythonanywhere.com
TIME_ZONE=America/Fortaleza
CROSSREF_ENRICH=True
CROSSREF_MAILTO=seu-email-real@example.com
```

O `.env` está ignorado pelo Git. Não o envie ao GitHub.

## 5. Preparar banco, conta administrativa e arquivos estáticos

```bash
workon citarn-venv
cd ~/citarn
python manage.py check --deploy
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 6. Criar o aplicativo web

Na aba **Web**:

1. escolha **Add a new web app**;
2. selecione **Manual configuration**;
3. escolha a mesma versão do Python do ambiente virtual;
4. em **Virtualenv**, informe `/home/SEUUSUARIO/.virtualenvs/citarn-venv`;
5. abra o arquivo de configuração WSGI e substitua seu conteúdo pelo bloco abaixo.

```python
import os
import sys

project_home = "/home/SEUUSUARIO/citarn"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "citarn.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

O próprio projeto carrega `~/citarn/.env` antes de ler as configurações.

## 7. Arquivos estáticos e uploads

O WhiteNoise já serve o CSS e o JavaScript coletados. Mesmo assim, o mapeamento nativo do PythonAnywhere é mais eficiente. Na seção **Static files**, adicione:

| URL | Diretório |
| --- | --- |
| `/static/` | `/home/SEUUSUARIO/citarn/staticfiles` |

Não crie um mapeamento público para `/media/`. Os arquivos enviados são entregues pela rota autenticada do CitaRN, o que impede que um usuário adivinhe o endereço do arquivo de outro.

Crie os diretórios, se necessário:

```bash
mkdir -p ~/citarn/media ~/citarn/staticfiles
chmod 700 ~/citarn/media
```

## 8. Ativar

Volte à aba **Web** e clique em **Reload**. Acesse:

```text
https://SEUUSUARIO.pythonanywhere.com
```

Teste, nesta ordem:

1. criar uma conta comum;
2. criar dois projetos;
3. importar um DOCX e um PDF;
4. importar um DOI;
5. revisar uma referência;
6. gerar a lista em ABNT e APA;
7. baixar DOCX e PDF;
8. confirmar que uma segunda conta não enxerga os dados da primeira.

## 9. URLs em conta gratuita

O PythonAnywhere encaminha o acesso externo das contas gratuitas por uma lista de permissões. `api.crossref.org` e `doi.org` constam na lista em agosto de 2026, então a importação por DOI deve funcionar. Uma página de periódico fora da lista pode retornar bloqueio; o CitaRN a cadastra para preenchimento manual, sem interromper o projeto.

## 10. Atualizações futuras

No Bash Console:

```bash
workon citarn-venv
cd ~/citarn
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

Depois, clique em **Reload** na aba Web.

## 11. Backup mínimo

Com SQLite, copie o banco apenas após garantir que não há uma gravação em andamento:

```bash
cd ~/citarn
python manage.py dumpdata --natural-foreign --natural-primary --indent 2 > ~/backup-citarn.json
tar -czf ~/backup-citarn-media.tar.gz media
```

Não envie backups, `.env`, banco ou uploads ao GitHub.

## 12. Quando migrar do PythonAnywhere gratuito

Considere um plano pago ou outra infraestrutura quando ocorrer um destes sinais:

- acervo se aproximando do limite de armazenamento;
- múltiplos usuários importando arquivos ao mesmo tempo;
- necessidade de acessar livremente qualquer URL;
- necessidade de antivírus, filas assíncronas, OCR ou processamento pesado;
- obrigação institucional de banco gerenciado, backups automáticos e auditoria ampliada.

Até esse ponto, Django + SQLite + PythonAnywhere é uma combinação econômica, transparente e sem dependência de Supabase ou Firebase.
