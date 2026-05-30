# Application Design: Budget-Naz

## Components

### 1. Model — `app/models/budget.py`
- BudgetEntry: id, date(unique), capital, sales, profit, tithes, total_income, total_deductions, net_income, created_at

### 2. Schema — `app/schemas/budget.py`
- BudgetCreate: date, capital, sales
- BudgetResponse: all fields

### 3. Router — `app/routers/budget.py`
- POST /api/budget/ — create (auto-compute)
- GET /api/budget/ — list all
- PUT /api/budget/{id} — update (recompute)
- DELETE /api/budget/{id} — delete

### 4. Template — `app/templates/pages/budget.html`
- Form: date, capital, sales
- Table with all columns + totals row
- Edit/Delete per row

## Computation
```
profit = sales - capital
tithes = profit * 0.10 if profit > 0 else 0
total_income = sales
total_deductions = capital + tithes
net_income = sales - capital - tithes
```
