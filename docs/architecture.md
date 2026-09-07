# Architecture

## Cloud Mapping (Huawei)

- **Compute**:
  - ECS (VM-based container hosting) or
  - CCE (Kubernetes-managed container orchestration)
- **Database**:
  - Huawei Cloud RDS for PostgreSQL (`DATABASE_URL`)
- **File Storage**:
  - Huawei OBS via `esdk-obs-python` adapter (`app/services/huawei_obs.py`)
- **Identity & API Security**:
  - Platform-level IAM token flow (`app/services/huawei_iam.py`)
- **AI/NLP Layer**:
  - ModelArts endpoint integration stub (`app/services/modelarts.py`)
- **Serverless Scoring Option**:
  - FunctionGraph-ready handler (`app/matching/functiongraph_handler.py`)

## Runtime Topology

1. Web (Next.js) and Mobile (Expo) call FastAPI REST API
2. FastAPI services persist domain data to PostgreSQL (RDS-compatible)
3. File assets are uploaded to OBS using signed URL pattern
4. Skill extraction can call ModelArts model endpoint through IAM token
5. Matching logic can run in API service or be deployed to FunctionGraph

## Financial data boundary

Sensitive personal and financial data remains off-chain. Database and object
storage encryption at rest is required from the platform provider; the
backend also supports Fernet field-level encryption through
`DATA_ENCRYPTION_KEY`. Blockchain integrations may store only an integrity
proof and non-sensitive reference, never account credentials, KYC documents,
or transaction secrets.

Production schema changes use Alembic migrations. Runtime startup must not be
used to mutate production schemas.
