from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WorkerProfile(Base):
    __tablename__ = "worker_profiles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    township: Mapped[str] = mapped_column(String(120), nullable=False)
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    resume_obs_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
