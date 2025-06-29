import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Index, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .relationships import group_users, user_roles

if TYPE_CHECKING:
    from .group import Group
    from .role import Role


class User(Base):
    __tablename__ = "users"
    __table_args__ = (Index("ix_user_email", "email"),)

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=user_roles, back_populates="users"
    )
    groups: Mapped[list["Group"]] = relationship(
        "Group", secondary=group_users, back_populates="users"
    )
