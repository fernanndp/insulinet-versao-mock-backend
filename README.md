# Insulinet Backend

API REST do **Insulinet**, uma aplicaÃ§Ã£o para controle de estoque de insulina, registro de doses e estimativa de autonomia com base no histÃ³rico de consumo.

## ProduÃ§Ã£o

- Aplicação: https://frontend-insulinet-mock.up.railway.app
- API: https://backend-insulinet-mock.up.railway.app
- Documentação da API: https://backend-insulinet-mock.up.railway.app/docs

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT
- Argon2
- Resend
- Railway

## Funcionalidades

- Cadastro e autenticaÃ§Ã£o de usuÃ¡rios
- RecuperaÃ§Ã£o e redefiniÃ§Ã£o de senha
- Cadastro e ediÃ§Ã£o de insulinas
- Controle de entradas e ajustes de estoque
- Registro individual e em lote de doses
- HistÃ³rico de movimentaÃ§Ãµes
- CÃ¡lculo do estoque atual
- Estimativa de consumo mÃ©dio
- ProjeÃ§Ã£o de dias restantes
- Isolamento dos dados por usuÃ¡rio

## Estrutura

```text
app/
â”œâ”€â”€ api/
â”‚   â””â”€â”€ routes/
â”‚       â”œâ”€â”€ auth.py
â”‚       â”œâ”€â”€ doses.py
â”‚       â”œâ”€â”€ health.py
â”‚       â”œâ”€â”€ insulins.py
â”‚       â”œâ”€â”€ stock.py
â”‚       â””â”€â”€ users.py
â”œâ”€â”€ core/
â”‚   â”œâ”€â”€ config.py
â”‚   â””â”€â”€ security.py
â”œâ”€â”€ services/
â”‚   â”œâ”€â”€ dose_service.py
â”‚   â”œâ”€â”€ email_service.py
â”‚   â”œâ”€â”€ insulin_service.py
â”‚   â”œâ”€â”€ projection_service.py
â”‚   â””â”€â”€ stock_service.py
â”œâ”€â”€ database.py
â”œâ”€â”€ main.py
â”œâ”€â”€ models.py
â””â”€â”€ schemas.py
```

A aplicaÃ§Ã£o separa as responsabilidades entre rotas HTTP, regras de negÃ³cio, seguranÃ§a, configuraÃ§Ã£o e persistÃªncia.

## ConfiguraÃ§Ã£o local

Clone o repositÃ³rio:

```bash
git clone https://github.com/fernanndp/insulinet-backend.git
cd insulinet-backend
```

Crie um ambiente virtual:

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependÃªncias:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` a partir do `.env.example`.

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/insulinet
APP_TIMEZONE=America/Fortaleza
JWT_SECRET_KEY=troque-por-uma-chave-secreta-forte
ACCESS_TOKEN_EXPIRE_MINUTES=1440
PASSWORD_RESET_EXPIRE_MINUTES=30
RESEND_API_KEY=
EMAIL_FROM=Insulinet <onboarding@resend.dev>
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Nunca versione o arquivo `.env`.

## Banco de dados

O projeto utiliza PostgreSQL e Alembic para controle de migrations.

```bash
alembic current
alembic heads
alembic upgrade head
```

## Executando localmente

```bash
uvicorn app.main:app --reload
```

API local:

```text
http://127.0.0.1:8000
```

DocumentaÃ§Ã£o interativa:

```text
http://127.0.0.1:8000/docs
```

## Principais endpoints

### AutenticaÃ§Ã£o

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

### UsuÃ¡rio

```text
GET /api/users/me
```

### Insulinas

```text
POST  /api/insulins
GET   /api/insulins
PATCH /api/insulins/{insulin_id}
GET   /api/insulins/{insulin_id}/history
GET   /api/insulins/{insulin_id}/summary
```

### Estoque

```text
POST  /api/insulins/{insulin_id}/stock
GET   /api/insulins/{insulin_id}/stock
POST  /api/insulins/{insulin_id}/adjustments
PATCH /api/insulins/{insulin_id}/stock/{movement_id}
```

### Doses

```text
POST  /api/insulins/{insulin_id}/doses
PATCH /api/insulins/{insulin_id}/doses/{dose_id}
POST  /api/insulins/{insulin_id}/dose-batches
```

## Deploy

O backend estÃ¡ hospedado no Railway com PostgreSQL gerenciado.

ConfiguraÃ§Ãµes principais de produÃ§Ã£o:

```text
Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT

Pre-deploy Command:
alembic upgrade head
```

As credenciais e demais valores sensÃ­veis sÃ£o configurados exclusivamente como variÃ¡veis de ambiente no Railway.

## SeguranÃ§a

- Hash de senhas com Argon2
- Tokens JWT para autenticaÃ§Ã£o
- AssociaÃ§Ã£o dos registros ao usuÃ¡rio autenticado
- VariÃ¡veis sensÃ­veis fora do controle de versÃ£o
- ConfiguraÃ§Ã£o explÃ­cita de CORS

## Roadmap

- Alertas de estoque baixo com base na autonomia estimada
- DefiniÃ§Ã£o de nÃ­vel mÃ­nimo de seguranÃ§a para reposiÃ§Ã£o
- PrevisÃ£o da data recomendada para aquisiÃ§Ã£o de nova unidade de insulina
- Controle do processo de reposiÃ§Ã£o diretamente pela plataforma
- Busca de opÃ§Ãµes de compra em farmÃ¡cias
- Redirecionamento para farmÃ¡cias ou pÃ¡ginas de compra compatÃ­veis
- PossÃ­vel integraÃ§Ã£o futura com serviÃ§os de disponibilidade e preÃ§os

A proposta Ã© evoluir o Insulinet de um sistema de controle de estoque para uma ferramenta capaz de antecipar a necessidade de reposiÃ§Ã£o e facilitar o acesso do usuÃ¡rio ao medicamento.

## Frontend

CÃ³digo-fonte:

https://github.com/fernanndp/insulinet-frontend

AplicaÃ§Ã£o:

https://insulinet-frontend-production.up.railway.app

## Status

Projeto em desenvolvimento e disponÃ­vel em ambiente de produÃ§Ã£o no Railway.

Versão mockada do Insulinet.
