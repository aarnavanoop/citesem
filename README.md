# CiteSem

CiteSem (Cite + Semester) is a web app for university students to turn their unit materials into a study tool. Students upload lecture slides, PDFs and notes, then ask questions and get answers with cited sources (file and page). It will also generate quizzes and schedule flashcard reviews using spaced repetition (SM-2). Under the hood it is built like a production system: an ingestion and cleaning pipeline, hybrid (vector + keyword) retrieval, background workers, an authenticated REST API, automated RAG evaluation, and infrastructure as code on AWS. It is built for students, tested with real classmates, and every part is something I can explain and rebuild from scratch.



## Status

Sprint 1 of 7 (Foundations). Work in progress.

| Area | Status |
|---|---|
| FastAPI app, `/health`, `/version` | Done |
| Docker + Docker Compose (API + Postgres) | Done |
| Database models and Alembic migrations | Done |
| Courses CRUD (scoped to owner) | Done |
| Register / login (argon2 + JWT) | Planned (20 Oct) |
| Tests and CI | Planned (22-24 Oct) |
| Ingestion pipeline, RAG, quizzes, flashcards | Planned (Sprints 2-4) |
| Terraform, CI/CD, monitoring, deploy to AWS | Planned (Sprints 5-6) |

## Tech stack

- **API:** Python 3.13, FastAPI, Pydantic
- **Database:** PostgreSQL 16, SQLAlchemy 2.0, Alembic
- **Tooling:** uv, Docker, Docker Compose, ruff, pytest
- **Planned:** Redis + RQ, S3, pgvector, sentence-transformers, Claude API, React, Terraform, GitHub Actions, AWS (ECS Fargate, RDS)

## Running locally

### Prerequisites

- [uv](https://docs.astral.sh/uv/)
- [Docker](https://docs.docker.com/get-docker/) with Docker Compose

### Setup

1. Clone the repo and create your environment file:

   ```bash
   cp .env.example .env
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Start Postgres:

   ```bash
   docker compose up -d postgres
   ```

4. Apply database migrations:

   ```bash
   uv run alembic upgrade head
   ```

5. Run the API with auto-reload:

   ```bash
   uv run fastapi dev app/main.py
   ```

The API is now at <http://localhost:8000> and interactive docs are at <http://localhost:8000/docs>.

### Run everything in Docker

```bash
docker compose up --build
```

This builds the API image and runs both the API and Postgres in containers.

### Useful commands

```bash
docker compose stop                 # stop containers, keep data
docker compose ps                   # see what is running
uv run alembic revision --autogenerate -m "describe change"   # new migration
uv run alembic upgrade head         # apply migrations
```

## Project structure

```
app/
├── main.py            # creates the app, includes routers, /health and /version
├── config.py          # settings read from environment variables
├── database.py        # engine, session factory, get_db dependency
├── models.py          # SQLAlchemy models (database tables)
├── schemas.py         # Pydantic schemas (request/response shapes)
├── dependencies.py    # shared dependencies such as get_current_user
└── routers/
    └── courses.py     # /courses endpoints
alembic/               # database migrations
docs/
└── learning-log.md    # what I built, what confused me, what I learned
```

## API (current)

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/version` | App version |
| POST | `/courses` | Create a course |
| GET | `/courses` | List my courses |
| GET | `/courses/{id}` | Get one course |
| PATCH | `/courses/{id}` | Update a course |
| DELETE | `/courses/{id}` | Delete a course |

Every course query filters by owner in the SQL itself, so one user can never read another user's data.

## Roadmap

| Sprint | Theme |
|---|---|
| 1 | Foundations: Git, API, Postgres, auth, tests, CI |
| 2 | Ingestion pipeline: S3, Redis, worker, data cleaning |
| 3 | RAG: embeddings, pgvector, hybrid search, streaming answers |
| 4 | Evaluation, quizzes, flashcards (SM-2), caching, rate limiting |
| 5 | Terraform on AWS, CI/CD, OIDC |
| 6 | Observability, load testing, security hardening |
| 7 | Real-user beta, polish, launch |

## Engineering practices

- Every change goes through a branch and a pull request, then a squash merge
- Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- Schema changes only through Alembic migrations
- Architecture decisions recorded in `docs/adr/`

## Author

Aarnav Anoop