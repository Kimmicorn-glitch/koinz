# Contributing

## Branching

- `feat/backend-*`
- `feat/web-*`
- `feat/mobile-*`
- `feat/docs-*`

## API Change Workflow

1. Update backend schema/routes
2. Update `shared/contracts/openapi.yaml`
3. Update `shared/types/api.ts`
4. Verify web/mobile clients still compile

## Pull Request Checklist

- [ ] Docker build passes for affected services
- [ ] New environment variables documented in `.env.example`
- [ ] Role access behavior reviewed for protected routes
- [ ] Docs updated when architecture/deployment changes
