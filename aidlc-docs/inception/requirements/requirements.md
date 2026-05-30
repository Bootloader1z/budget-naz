# Requirements: Budget-Naz

## Intent Analysis
- **Type**: New Project (Greenfield)
- **Scope**: Single-page budgeting app
- **Complexity**: Simple

## Business Logic (Priority Order)
1. **Capital** — Input: money invested/spent to produce goods
2. **Sales** — Input: total revenue received
3. **Profit** = Sales - Capital
4. **Tithes** = 10% of Profit (only if profit > 0)
5. **Total Income** = Sales
6. **Total Deductions** = Capital + Tithes
7. **Net Income** = Sales - Capital - Tithes

## Functional Requirements

### FR-01: Daily Budget Entry
- User inputs: date, capital, sales
- System auto-computes: profit, tithes, total_income, total_deductions, net_income
- Date defaults to today

### FR-02: Budget Table
- Columns: Date | Capital | Sales | Profit | Tithes (10%) | Total Income | Total Deductions | Net Income | Actions
- Sorted by date descending
- Totals row at bottom

### FR-03: CRUD
- Create, Read, Update, Delete entries
- Edit recomputes all derived fields

## Non-Functional Requirements
- SQLite database (no external DB needed)
- Single-page UI with Jinja2 template
- No authentication required (personal use)
