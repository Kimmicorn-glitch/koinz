# Shared

Shared API assets consumed by both web and mobile apps.

## Contents

- `contracts/openapi.yaml`: API contract source of truth
- `types/api.ts`: shared request/response TypeScript interfaces

## Contract Sync Rule

When backend schema changes:

1. Update FastAPI schema/models
2. Update `shared/contracts/openapi.yaml`
3. Update `shared/types/api.ts`
4. Validate web/mobile clients compile against updated types
