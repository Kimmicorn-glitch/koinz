from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Local Hands 2.0 API"
    app_version: str = "2.0.0"
    environment: str = "development"

    database_url: str = "postgresql+psycopg://postgres:postgres@postgres:5432/local_hands"

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    security_headers_enabled: bool = True
    rate_limit_login_per_minute: int = 10
    rate_limit_payments_per_minute: int = 60
    allowed_origins: str = "http://localhost:3000"
    data_encryption_key: str = ""

    default_employer_email: str = "employer@localhands.com"
    default_employer_password: str = "ChangeMe123!"
    default_worker_email: str = "worker@localhands.com"
    default_worker_password: str = "ChangeMe123!"

    # Huawei Cloud RDS / networking
    huawei_project_id: str = ""
    huawei_region: str = "af-south-1"

    # Huawei OBS
    huawei_obs_endpoint: str = "https://obs.af-south-1.myhuaweicloud.com"
    huawei_obs_access_key: str = ""
    huawei_obs_secret_key: str = ""
    huawei_obs_bucket: str = "local-hands-assets"

    # Huawei IAM / API integration
    huawei_iam_endpoint: str = "https://iam.myhuaweicloud.com/v3/auth/tokens"
    huawei_iam_domain_name: str = ""
    huawei_iam_username: str = ""
    huawei_iam_password: str = ""

    # ModelArts NLP endpoint (placeholder wiring)
    modelarts_skill_endpoint: str = ""

    # Payments (PSP integration placeholders)
    psp_provider: str = "mock"
    psp_api_key: str = ""
    psp_webhook_secret: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def normalize_origins(cls, value: str | list[str]) -> str:
        if isinstance(value, list):
            return ",".join(value)
        return value

    def validate_production_security(self) -> None:
        if self.environment.lower() not in {"production", "prod"}:
            return
        if self.jwt_secret_key == "change-me" or len(self.jwt_secret_key) < 32:
            raise RuntimeError("JWT_SECRET_KEY must be a strong production secret")
        if not self.data_encryption_key:
            raise RuntimeError("DATA_ENCRYPTION_KEY is required in production")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


settings = Settings()
