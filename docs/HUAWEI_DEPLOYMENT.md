# Huawei Cloud Deployment

## 1) Build and Tag Images

```bash
# backend
cd backend
docker build -t local-hands-backend:2.0.0 .

# web
cd ../web-app
docker build -t local-hands-web:2.0.0 .
```

## 2) Push to Huawei SWR

```bash
# Example registry format:
# swr.<region>.myhuaweicloud.com/<org>/<image>:<tag>

docker tag local-hands-backend:2.0.0 swr.af-south-1.myhuaweicloud.com/<org>/local-hands-backend:2.0.0
docker tag local-hands-web:2.0.0 swr.af-south-1.myhuaweicloud.com/<org>/local-hands-web:2.0.0

# Authenticate and push
# (Use Huawei Cloud console credentials / temporary login token)
docker login swr.af-south-1.myhuaweicloud.com
docker push swr.af-south-1.myhuaweicloud.com/<org>/local-hands-backend:2.0.0
docker push swr.af-south-1.myhuaweicloud.com/<org>/local-hands-web:2.0.0
```

## 3) Deploy on ECS (VM Path)

1. Create ECS VM in same VPC/subnet as RDS.
2. Install Docker + Docker Compose.
3. Pull images from SWR.
4. Provide `.env` with production values.
5. Run containers and attach Nginx using `docker/nginx.ecs.conf`.

### Required ECS Security Group Rules

- Inbound 80/443 from internet (web)
- Inbound 22 from admin IP (SSH)
- Backend container port `8000` only from local host / internal network
- Outbound to RDS and OBS endpoints

## 4) Deploy on CCE (Kubernetes Path)

1. Create CCE cluster (same VPC as RDS).
2. Add SWR image pull permissions.
3. Create Kubernetes secrets for env and OBS/IAM credentials.
4. Deploy backend and web deployments/services.
5. Expose via ingress with TLS.

```bash
kubectl apply -f docker/cce-backend-deployment.yaml
kubectl apply -f docker/cce-web-deployment.yaml
```

## 5) Connect RDS PostgreSQL

- Set `DATABASE_URL=postgresql+psycopg://<user>:<pass>@<rds-private-ip>:5432/<db>`
- Allow inbound 5432 to RDS from ECS/CCE subnet security group only.

## 6) Configure OBS + IAM + ModelArts

Set these vars in runtime secret store:

- `HUAWEI_OBS_ENDPOINT`
- `HUAWEI_OBS_ACCESS_KEY`
- `HUAWEI_OBS_SECRET_KEY`
- `HUAWEI_OBS_BUCKET`
- `HUAWEI_IAM_ENDPOINT`
- `HUAWEI_IAM_DOMAIN_NAME`
- `HUAWEI_IAM_USERNAME`
- `HUAWEI_IAM_PASSWORD`
- `HUAWEI_PROJECT_ID`
- `MODELARTS_SKILL_ENDPOINT`

## 7) FunctionGraph Option

Deploy `app/matching/functiongraph_handler.py` as FunctionGraph function to offload matching score computation serverlessly.
