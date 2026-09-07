from obs import ObsClient

from app.core.config import settings


class HuaweiOBSStorage:
    def __init__(self) -> None:
        self.client = ObsClient(
            access_key_id=settings.huawei_obs_access_key,
            secret_access_key=settings.huawei_obs_secret_key,
            server=settings.huawei_obs_endpoint,
        )

    def create_presigned_upload_url(self, object_key: str, expires_seconds: int = 900) -> str:
        response = self.client.createSignedUrl(
            method="PUT",
            bucketName=settings.huawei_obs_bucket,
            objectKey=object_key,
            expires=expires_seconds,
        )
        if response.status >= 300:
            raise RuntimeError(f"OBS signed URL creation failed: {response.errorMessage}")
        return response.signedUrl

    def shutdown(self) -> None:
        self.client.close()
