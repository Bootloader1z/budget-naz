from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.budget import Capital, IncomeEntry, CapitalAudit
from app.schemas.budget import (
    CapitalResponse, CapitalSet,
    AuditResponse,
    IncomeCreate, IncomeResponse,
    ComputedRow, BudgetSummary,
)

router = APIRouter(prefix="/api/budget", tags=["budget"])


@router.get("/capital", response_model=CapitalResponse)
def get_capital(db: Session = Depends(get_db)):
    cap = db.query(Capital).first()
    if not cap:
        cap = Capital(amount=0)
        db.add(cap)
        db.commit()
        db.refresh(cap)
    return cap


@router.put("/capital", response_model=CapitalResponse)
def set_capital(body: CapitalSet, db: Session = Depends(get_db)):
    cap = db.query(Capital).first()
    if cap:
        audit = CapitalAudit(old_amount=cap.amount, new_amount=body.amount, reason=body.reason)
        db.add(audit)
        cap.amount = body.amount
    else:
        cap = Capital(amount=body.amount)
        db.add(cap)
    db.commit()
    db.refresh(cap)
    return cap


@router.get("/audit", response_model=list[AuditResponse])
def list_audit(db: Session = Depends(get_db)):
    return db.query(CapitalAudit).order_by(CapitalAudit.changed_at.desc()).all()


@router.post("/income", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(body: IncomeCreate, db: Session = Depends(get_db)):
    entry = IncomeEntry(**body.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/income", response_model=list[IncomeResponse])
def list_income(db: Session = Depends(get_db)):
    return db.query(IncomeEntry).order_by(IncomeEntry.date.asc()).all()


@router.put("/income/{entry_id}", response_model=IncomeResponse)
def update_income(entry_id: int, body: IncomeCreate, db: Session = Depends(get_db)):
    entry = db.query(IncomeEntry).filter(IncomeEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Income entry not found")
    entry.income = body.income
    entry.note = body.note
    entry.date = body.date
    entry.payment_method = body.payment_method
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/income/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(IncomeEntry).filter(IncomeEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Income entry not found")
    db.delete(entry)
    db.commit()


def _compute_rows(db: Session) -> tuple[float, list[dict]]:
    cap = db.query(Capital).first()
    capital_amount = cap.amount if cap else 0
    entries = db.query(IncomeEntry).order_by(IncomeEntry.date.asc()).all()
    rows = []
    running = capital_amount
    for e in entries:
        if running > 0:
            capital_repaid = min(e.income, running)
            running -= capital_repaid
            profit = e.income - capital_repaid
        else:
            capital_repaid = 0
            profit = e.income
        tithes = profit * 0.10 if profit > 0 else 0
        clean = profit - tithes
        rows.append({
            "id": e.id, "date": e.date, "income": e.income, "note": e.note,
            "capital_repaid": capital_repaid, "remaining_capital": running,
            "profit": profit, "tithes": tithes, "clean": clean,
            "payment_method": e.payment_method,
        })
    return capital_amount, rows


@router.get("/computed", response_model=list[ComputedRow])
def get_computed(db: Session = Depends(get_db)):
    _, rows = _compute_rows(db)
    return rows


@router.get("/summary", response_model=BudgetSummary)
def get_summary(db: Session = Depends(get_db)):
    capital_amount, rows = _compute_rows(db)
    total_income = sum(r["income"] for r in rows)
    total_capital_repaid = sum(r["capital_repaid"] for r in rows)
    total_profit = sum(r["profit"] for r in rows)
    total_tithes = sum(r["tithes"] for r in rows)
    total_clean = sum(r["clean"] for r in rows)
    entry_count = len(rows)
    return {
        "capital": capital_amount,
        "total_income": total_income,
        "total_capital_repaid": total_capital_repaid,
        "remaining_capital": capital_amount - total_capital_repaid,
        "total_profit": total_profit,
        "total_tithes": total_tithes,
        "total_clean": total_clean,
        "average_income": total_income / entry_count if entry_count > 0 else 0,
        "entry_count": entry_count,
    }
