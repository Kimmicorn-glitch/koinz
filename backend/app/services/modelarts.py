import httpx

from app.core.config import settings
from app.services.huawei_iam import HuaweiIAMClient


class ModelArtsSkillExtractor:
    def __init__(self) -> None:
        self.endpoint = settings.modelarts_skill_endpoint
        self.iam = HuaweiIAMClient()

    def extract_skills(self, text: str) -> list[str]:
        if not self.endpoint:
            # Placeholder path is integrated and can be enabled by setting MODELARTS_SKILL_ENDPOINT.
            return []

        token = self.iam.issue_token()
        headers = {"X-Auth-Token": token}
        payload = {"text": text}

        response = httpx.post(self.endpoint, json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        data = response.json()

        # TODO: Align parsing with deployed ModelArts custom model response contract.
        return data.get("skills", [])
