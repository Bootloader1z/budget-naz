from datetime import date, datetime, timezone
from sqlalchemy import Float, Date, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Capital(Base):
    __tablename__ = "capital"
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class IncomeEntry(Base):
    __tablename__ = "income_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    income: Mapped[float] = mapped_column(Float)
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True, default="Cash")
    note: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CapitalAudit(Base):
    __tablename__ = "capital_audit"
    id: Mapped[int] = mapped_column(primary_key=True)
    old_amount: Mapped[float] = mapped_column(Float)
    new_amount: Mapped[float] = mapped_column(Float)
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
