# CitaRN

Gerenciador web de referências acadêmicas construído em Django. Cada usuário possui uma biblioteca privada, pode criar vários projetos, importar fontes em PDF, DOCX, PPTX ou por URL/DOI, revisar os metadados e gerar listas em diferentes estilos bibliográficos.

## O que já está implementado

- cadastro, login e separação integral dos dados por usuário;
- múltiplos projetos por conta;
- biblioteca pessoal reutilizável entre projetos;
- importação simultânea de PDF, DOCX e PPTX;
- importação de URLs, páginas acadêmicas e DOI;
- enriquecimento opcional pelo Crossref quando um DOI é encontrado;
- detecção de duplicatas por DOI ou impressão digital dos metadados;
- revisão manual de todos os campos bibliográficos;
- referências ABNT NBR 6023:2018, APA 7, Vancouver, Chicago autor-data, Harvard e IEEE;
- seleção independente das referências de cada projeto;
- exportação em DOCX, PDF e TXT;
- arquivo original protegido por autenticação;
- interface responsiva e acessível;
- painel administrativo do Django;
- testes automatizados e verificação contínua no GitHub.

## Arquitetura

O projeto usa uma aplicação Django monolítica, adequada ao PythonAnywhere e fácil de manter:

```text
Navegador
   │
   ▼
Django ── autenticação, projetos, biblioteca, formatação e exportação
   │
   ├── SQLite (implantação inicial) ou MySQL (crescimento)
   ├── armazenamento local protegido dos arquivos enviados
   └── Crossref (somente para enriquecimento por DOI; falha de forma segura)
```

Não há dependência de Supabase, Firebase ou de serviços de IA. O sistema continua funcionando mesmo quando uma URL externa ou o Crossref não estão disponíveis; nesse caso, a fonte é salva para preenchimento manual.

## Instalação local

Requer Python 3.11 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`.

Para criar uma conta e dados demonstrativos:

```bash
python manage.py seed_demo --username demo --password 'UmaSenhaForte123!'
```

## Testes e validações

```bash
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```

Os testes cobrem formatação, extração de metadados, isolamento entre usuários, importação de DOCX, seleção por projeto e exportação.

## Configuração

Copie `.env.example` para `.env`. As variáveis mais importantes são:

| Variável | Uso |
| --- | --- |
| `SECRET_KEY` | chave criptográfica do Django; obrigatória em produção |
| `DEBUG` | deve ser `False` em produção |
| `ALLOWED_HOSTS` | domínio público do aplicativo |
| `CSRF_TRUSTED_ORIGINS` | origem HTTPS do aplicativo |
| `CROSSREF_ENRICH` | ativa ou desativa o enriquecimento por DOI |
| `CROSSREF_MAILTO` | e-mail de contato recomendado pela etiqueta da API Crossref |
| `MAX_UPLOAD_FILE_SIZE` | limite por arquivo, em bytes |
| `MEDIA_ROOT` | diretório persistente dos arquivos enviados |

O banco padrão é SQLite. Para MySQL, instale `requirements-mysql.txt` e preencha as variáveis `DB_*` do exemplo.

## Implantação

As instruções completas e verificadas para o PythonAnywhere estão em [docs/DEPLOY_PYTHONANYWHERE.md](docs/DEPLOY_PYTHONANYWHERE.md).

## Limites conscientes

- A extração depende dos metadados incorporados e do texto legível do arquivo. PDF digitalizado como imagem pode exigir preenchimento manual.
- ABNT e outros estilos possuem casos especiais por tipo de documento e por instituição. A lista gerada deve passar por revisão final antes da submissão.
- Contas gratuitas novas do PythonAnywhere possuem 512 MiB de armazenamento e um único processo web. Para acervos grandes, é necessário planejar limpeza, backup ou mudança de plano.
- Na conta gratuita, a consulta de URLs externas é limitada à lista de domínios permitidos do PythonAnywhere. DOI e Crossref constam nessa lista; páginas não permitidas são cadastradas para revisão manual.

## Segurança e privacidade

- Todas as consultas de projetos, referências e arquivos são filtradas pelo proprietário autenticado.
- Downloads de arquivos enviados passam por uma rota autenticada; não são expostos como links públicos em produção.
- URLs são validadas contra endereços locais, privados e reservados antes de qualquer tentativa de acesso.
- Tipos e tamanhos de upload são limitados.
- Segredos e banco local não entram no Git.

Consulte [SECURITY.md](SECURITY.md) antes de colocar o sistema em produção.

## Autoria

Desenvolvido por Rodrigo Niskier.

Código preparado para uso privado. A definição de uma licença pública pode ser feita posteriormente, caso o repositório seja aberto.
