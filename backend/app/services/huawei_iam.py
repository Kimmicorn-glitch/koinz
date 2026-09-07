import httpx

from app.core.config import settings


class HuaweiIAMClient:
    def __init__(self) -> None:
        self.endpoint = settings.huawei_iam_endpoint

    def issue_token(self) -> str:
        payload = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": settings.huawei_iam_username,
                            "password": settings.huawei_iam_password,
                            "domain": {"name": settings.huawei_iam_domain_name},
                        }
                    },
                },
                "scope": {"project": {"id": settings.huawei_project_id}},
            }
        }

        response = httpx.post(self.endpoint, json=payload, timeout=20.0)
        response.raise_for_status()

        token = response.headers.get("X-Subject-Token")
        if not token:
            raise RuntimeError("IAM token not found in response headers")
        return token
