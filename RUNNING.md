# Running Local Hands (Demo Guide)

This guide shows the fastest way to run the full app for a demo.

## 1) Prerequisites

- Ubuntu/macOS/Windows (WSL works)
- Docker Engine installed
- Docker Compose v2 installed

Verify:

```bash
docker --version
docker compose version
```

If Docker permission is denied on Linux:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 2) Start the application

From project root:

```bash
cd /home/kimbez/LocalHands/local-hands
cp .env.example .env
docker compose -f docker/docker-compose.yml up --build -d
```

Check services:

```bash
docker compose -f docker/docker-compose.yml ps
```

Expected running services:

- `lh-postgres` (port `5432`)
- `lh-backend` (port `8000`)
- `lh-web` (port `3000`)
- `lh-mobile` (port `8081`)

## 3) Demo URLs

- Web app: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Mobile Expo dev server: http://localhost:8081

## 4) Demo login accounts

- Employer: `employer@localhands.com` / `ChangeMe123!`
- Worker: `worker@localhands.com` / `ChangeMe123!`

## 5) Quick health checks

```bash
curl -I http://localhost:3000
curl -I http://localhost:8000/docs
```

`HTTP/1.1 200` means healthy.

## 6) Useful runtime commands

Tail backend logs:

```bash
docker compose -f docker/docker-compose.yml logs -f backend
```

Restart backend:

```bash
docker compose -f docker/docker-compose.yml restart backend
```

Stop all services:

```bash
docker compose -f docker/docker-compose.yml down
```

Stop and remove volumes (fresh DB reset):

```bash
docker compose -f docker/docker-compose.yml down -v
```

## 7) Common issues

1. `permission denied ... /var/run/docker.sock`

Run:

```bash
newgrp docker
```

Then retry compose command.

2. Login page keeps failing after backend fixes

- Hard refresh browser: `Ctrl+Shift+R`
- Check backend logs for errors:

```bash
docker compose -f docker/docker-compose.yml logs --tail=200 backend
```

3. Port already in use (`3000`, `8000`, `5432`, `8081`)

- Stop conflicting process or run:

```bash
docker compose -f docker/docker-compose.yml down
```

Then start again.
