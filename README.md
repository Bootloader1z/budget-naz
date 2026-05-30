# 💰 Budget-Naz

Personal budgeting system with capital tracking, POS-style income entries, and automated profit/tithes computation.

## How It Works

1. **Set your capital** (one-time investment in your business)
2. **Add daily income** entries (like a POS — multiple per day, with payment method)
3. **System auto-computes**:
   - Income repays capital first (priority #1)
   - Once capital is fully repaid, income becomes profit
   - Tithes = 10% of profit (auto-deducted)
   - Clean = profit after tithes

## Architecture

```
budget-naz/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── database.py          # SQLite + SQLAlchemy setup
│   ├── models/
│   │   └── budget.py        # Capital, IncomeEntry, CapitalAudit models
│   ├── schemas/
│   │   └── budget.py        # Pydantic request/response schemas
│   ├── routers/
│   │   └── budget.py        # API endpoints + computation logic
│   └── templates/
│       └── pages/
│           └── budget.html   # Single-page UI (dark theme)
├── static/css/
│   └── style.css            # Print styles
├── aidlc-docs/              # AI-DLC development documentation
├── requirements.txt
└── README.md
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12 + FastAPI |
| Database | SQLite (file-based, zero config) |
| ORM | SQLAlchemy 2.0 |
| Frontend | Vanilla JS + CSS (no frameworks) |
| Styling | Custom dark/light theme with CSS variables |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard UI |
| GET | `/api/budget/capital` | Get current capital |
| PUT | `/api/budget/capital` | Set/update capital (with audit) |
| GET | `/api/budget/audit` | Capital change history |
| POST | `/api/budget/income` | Add income entry |
| GET | `/api/budget/income` | List all income entries |
| PUT | `/api/budget/income/{id}` | Update income entry |
| DELETE | `/api/budget/income/{id}` | Delete income entry |
| GET | `/api/budget/computed` | Full budget breakdown table |
| GET | `/api/budget/summary` | Aggregated totals |

## Setup & Run

```bash
# Clone
git clone https://github.com/Bootloader1z/budget-naz.git
cd budget-naz

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Open `http://localhost:8001` in your browser.

## Features

- **Capital Tracking** — Set once, editable with full audit trail
- **POS-Style Entries** — Multiple income entries per day
- **Payment Methods** — Cash, GCash, Bank Transfer, Other
- **Auto-Computation** — Capital repayment → Profit → Tithes → Clean
- **Dark/Light Theme** — Toggle between themes
- **Custom Date Picker** — Modern calendar popup
- **Month Filter** — Filter entries by month
- **Export CSV** — Download data as CSV
- **Export PDF** — Professional print-ready report
- **Toast Notifications** — Success/error feedback
- **Responsive** — Works on mobile and desktop
- **Enter Key Submit** — Quick entry via keyboard

## Business Logic

```
Priority Order:
1. Income → Repay Capital (until capital balance = 0)
2. Remaining Income → Profit
3. Profit × 10% → Tithes (deducted)
4. Profit - Tithes → Clean (your take-home)
```

### Example

Capital: ₱1,000

| Day | Income | Capital Repaid | Remaining | Profit | Tithes | Clean |
|-----|--------|---------------|-----------|--------|--------|-------|
| 1 | ₱300 | ₱300 | ₱700 | ₱0 | ₱0 | ₱0 |
| 2 | ₱400 | ₱400 | ₱300 | ₱0 | ₱0 | ₱0 |
| 3 | ₱500 | ₱300 | ₱0 ✅ | ₱200 | ₱20 | ₱180 |
| 4 | ₱600 | ₱0 | ₱0 | ₱600 | ₱60 | ₱540 |

## License

MIT
