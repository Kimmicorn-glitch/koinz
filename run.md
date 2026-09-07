# Run KOINZ locally

This guide starts the KOINZ services and verifies that the backend is healthy.

## Option 1: Docker Compose

Open PowerShell and run:

```powershell
cd "C:\Users\Pamela Nkonyane\Documents\LocalHands\koinz"

docker compose -f docker\docker-compose.yml up --build -d
docker compose -f docker\docker-compose.yml ps

$health = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
$health.StatusCode
$health.Content
```

The expected status is:

```text
200
```

The backend API documentation is available at:

```text
http://localhost:8000/docs
```

The web application is available at:

```text
http://localhost:3000
```

## Option 2: Backend only

If Docker is unavailable:

```powershell
cd "C:\Users\Pamela Nkonyane\Documents\LocalHands\koinz\backend"
\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

In a second PowerShell window:

```powershell
$health = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
$health.StatusCode
$health.Content
```

## Troubleshooting

View backend logs:

```powershell
cd "C:\Users\Pamela Nkonyane\Documents\LocalHands\koinz"
docker compose -f docker\docker-compose.yml logs --tail=200 backend
```

Stop the services:

```powershell
docker compose -f docker\docker-compose.yml down
```

`200` means the health endpoint responded successfully. It does not mean that
any financial transaction was executed or settled.
