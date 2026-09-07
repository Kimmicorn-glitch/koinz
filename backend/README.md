# Backend Service

Local Hands backend is a FastAPI-based microservices-in-a-monorepo implementation targeting Huawei Cloud deployment.

## Microservices Domains

- `app/auth`: JWT authentication and role-aware access control
- `app/profile`: worker profile creation and skill metadata
- `app/jobs`: employer job posting domain
- `app/matching`: weighted scoring + skill-gap engine
- `app/analytics`: platform analytics aggregations
- `app/services`: Huawei integrations (IAM, OBS, ModelArts)

## Extend Services

1. Add domain model in `app/<domain>/models.py`
2. Add Pydantic I/O contracts in `app/<domain>/schemas.py`
3. Implement business logic in `app/<domain>/service.py`
4. Expose route handlers in `app/<domain>/routes.py`
5. Register router in `app/api/routes/__init__.py`

## AI Integration Design

- ModelArts skill extraction lives in `app/services/modelarts.py`
- IAM token generation is handled by `app/services/huawei_iam.py`
- Matching logic is isolated in `app/matching/service.py`
- FunctionGraph-ready handler exists at `app/matching/functiongraph_handler.py`

## Local Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Database migrations

Schema changes must be delivered through Alembic migrations. From this
directory:

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe schema change"
```

The baseline revision records the existing schema history. Do not use
`Base.metadata.create_all()` in production deployments.

`DATA_ENCRYPTION_KEY` must be supplied by a secret manager for field-level
encryption. Generate a development key with:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Default seeded users:

- Employer: `employer@localhands.com / ChangeMe123!`
- Worker: `worker@localhands.com / ChangeMe123!`
