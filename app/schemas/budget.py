from datetime import date, datetime
from pydantic import BaseModel


class CapitalSet(BaseModel):
    amount: float
    reason: str | None = None


class CapitalResponse(BaseModel):
    id: int
    amount: float
    updated_at: datetime
    model_config = {"from_attributes": True}


class IncomeCreate(BaseModel):
    date: date
    income: float
    payment_method: str = "Cash"
    note: str | None = None


class IncomeResponse(BaseModel):
    id: int
    date: date
    income: float
    payment_method: str | None
    note: str | None
    created_at: datetime
    model_config = {"from_attributes": True}


class ComputedRow(BaseModel):
    id: int
    date: date
    income: float
    capital_repaid: float
    remaining_capital: float
    profit: float
    tithes: float
    clean: float
    payment_method: str | None
    note: str | None


class BudgetSummary(BaseModel):
    capital: float
    total_income: float
    total_capital_repaid: float
    remaining_capital: float
    total_profit: float
    total_tithes: float
    total_clean: float
    average_income: float
    entry_count: int


class AuditResponse(BaseModel):
    id: int
    old_amount: float
    new_amount: float
    reason: str | None
    changed_at: datetime
    model_config = {"from_attributes": True}
