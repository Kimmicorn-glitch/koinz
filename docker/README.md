# Docker

## Local Development

```bash
docker compose -f docker/docker-compose.yml up --build
```

Services:

- Backend: `http://localhost:8000`
- Web: `http://localhost:3000`
- Mobile (Expo): `http://localhost:8081`
- PostgreSQL: `localhost:5432`

## ECS Nginx Reverse Proxy

Use `docker/nginx.ecs.conf` on ECS host to route:

- `/api/*` -> backend container (`:8000`)
- `/` -> Next.js web container (`:3000`)
