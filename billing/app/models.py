import enum
import uuid
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import as_declarative, relationship
from typing import Any, List, Optional, Type, TypeVar


TBase = TypeVar("TBase", bound="Base")


@as_declarative()
class Base:
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow, nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    async def all(cls: Type[TBase], db: AsyncSession) -> List[TBase]:
        db_execute = await db.execute(sa.select(cls))
        return db_execute.scalars().all()

    @classmethod
    async def filter(cls: Type[TBase], db: AsyncSession, conditions: List[Any]) -> List[TBase]:
        conditions.append(cls.is_active == True)
        query = sa.select(cls)
        db_execute = await db.execute(query.where(sa.and_(*conditions)))
        return db_execute.scalars().all()

    @classmethod
    async def get_by_id(cls: Type[TBase], db: AsyncSession, object_id: int) -> Optional[TBase]:
        db_execute = await db.execute(sa.select(cls).where(cls.id == object_id))
        instance = db_execute.scalars().first()
        return instance

    async def save(self, db: AsyncSession) -> None:
        db.add(self)
        try:
            await db.flush()
        except Exception as exc:
            print(f"!!!!!!!!!!!!!!!!!{exc}")
        await db.refresh(self)

    async def update(self, db: AsyncSession, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await self.save(db)


class Position(enum.Enum):
    admin = "admin"
    accounting_clerk = "accounting_clerk"
    repairman = "repairman"
    employee = "employee"


class User(Base):
    __tablename__ = "users"
    public_id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=True)
    last_name = sa.Column(sa.String, nullable=True)
    position = sa.Column(ENUM(Position), unique=False, nullable=False)


class TransactionType(enum.Enum):
    income = "income"
    outcome = "outcome"


class Payment(Base):
    __tablename__ = "payments"
    amount = sa.Column(sa.Integer, nullable=False)
    type = sa.Column(ENUM(TransactionType), unique=False, nullable=False)
    user_id = relationship(User, lazy="selectin", back_populates="payments")
