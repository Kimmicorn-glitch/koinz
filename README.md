# Local Hands 2.0 - AI-Powered Township Employment Intelligence Platform

Production-ready monorepo skeleton targeting Huawei Cloud with shared REST API for web and mobile clients.

## Architecture Overview

```text
local-hands/
  backend/      FastAPI microservices domains + Huawei integrations
  web-app/      Next.js (App Router) + Tailwind dashboard UI
  mobile-app/   Expo + React Navigation mobile client
  shared/       OpenAPI contract + shared API types
  docker/       Compose stack + ECS nginx reverse proxy config
  docs/         Architecture, team tasks, Huawei deployment
```

## Cloud Mapping Diagram Explanation

- **Compute plane**: deploy backend/web containers to ECS (Docker Compose) or CCE (K8s)
- **Data plane**: backend persists to Huawei RDS PostgreSQL
- **Object storage**: backend uses Huawei OBS SDK for file upload flows
- **Identity plane**: Huawei IAM token flow support for cloud API calls
- **AI plane**: ModelArts endpoint integration path for NLP skill extraction
- **Serverless scoring**: matching handler is FunctionGraph-compatible

See: `docs/architecture.md` and `docs/HUAWEI_DEPLOYMENT.md`.

## Run Locally

```bash
cd local-hands
cp .env.example .env
docker compose -f docker/docker-compose.yml up --build
```

Local endpoints:

- Backend: `http://localhost:8000`
- Web: `http://localhost:3000`
- Mobile Expo: `http://localhost:8081`

## Huawei Cloud Deployment

1. Build backend/web Docker images.
2. Push images to Huawei SWR.
3. Provision RDS PostgreSQL.
4. Deploy to ECS (Docker) or CCE (Kubernetes).
5. Inject env vars for RDS/OBS/IAM/ModelArts.
6. Configure security groups and ingress.

Detailed runbook: `docs/HUAWEI_DEPLOYMENT.md`.

## Shared API Contract and Sync

- Primary contract: `shared/contracts/openapi.yaml`
- Shared types: `shared/types/api.ts`
- Required endpoints implemented:
  - `POST /auth/login`
  - `POST /profiles/`
  - `POST /jobs/`
  - `GET /matches/{job_id}`
  - `GET /analytics/overview`

## Team Development Workflow

1. Domain-specific branch (`feat/backend-*`, `feat/web-*`, `feat/mobile-*`)
2. Contract-first updates in `shared/contracts/openapi.yaml`
3. Keep web/mobile types aligned with `shared/types/api.ts`
4. Open PR with checklist from `docs/contributing.md`
5. Follow sprint assignments in `docs/TEAM_TASKS.md`
