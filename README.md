# 💧 Barrage-Flow Manager

> Smart dam management system for **Youssef Ibn Tachfine Dam**, Tiznit — Morocco.

Barrage-Flow Manager monitors water levels, distributes water fairly to farming cooperatives, prevents dangerous shortages, and maintains a full immutable audit trail — replacing manual paper-based processes with a reliable digital system.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [API Documentation](#api-documentation)
- [User Roles](#user-roles)
- [Business Rules](#business-rules)
- [Team Modules](#team-modules)
- [Contributing](#contributing)

---

## Overview

| | |
|---|---|
| **Project** | Barrage-Flow Manager |
| **Location** | Youssef Ibn Tachfine Dam, Tiznit — Morocco |
| **Version** | v1.0 |
| **Stack** | FastAPI · React · PostgreSQL · Redis · Docker |

### 5 Core System Jobs

| # | Job | Description |
|---|-----|-------------|
| 1 | **Monitor** | Read water level sensors every 15 min, display live |
| 2 | **Predict** | AI forecast of water level for next 6 months |
| 3 | **Distribute** | Fair-share formula for cooperative water allocation |
| 4 | **Protect** | Auto-block releases when safety reserve is too low |
| 5 | **Audit** | Immutable log of every action — who, what, when, why |

---

## Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — Database migrations
- [PostgreSQL](https://www.postgresql.org/) — Primary database
- [Redis](https://redis.io/) — Caching & real-time pub/sub
- [Celery](https://docs.celeryq.dev/) — Background task queue (sensor ingestion, ML jobs)
- [PyJWT](https://pyjwt.readthedocs.io/) — JWT authentication

**Frontend**
- [React 18](https://react.dev/) + [Vite](https://vitejs.dev/)
- [Zustand](https://zustand-demo.pmnd.rs/) — State management
- [React Query](https://tanstack.com/query) — Server state & caching
- [Recharts](https://recharts.org/) — Charts & forecasting graphs
- [Tailwind CSS](https://tailwindcss.com/) — Styling

**ML / AI**
- [scikit-learn](https://scikit-learn.org/) — Anomaly detection (Isolation Forest)
- [TensorFlow / Keras](https://www.tensorflow.org/) — LSTM forecasting, LSTM Autoencoder
- [DEAP](https://deap.readthedocs.io/) — NSGA-II optimization (allocation)
- [statsmodels](https://www.statsmodels.org/) — SARIMA ensemble

**Infrastructure**
- [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Actions](https://github.com/features/actions) — CI/CD

---

## Project Structure

```
barrage-flow-manager/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml        # Backend lint + test pipeline
│       └── frontend-ci.yml       # Frontend lint + test + build pipeline
│
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── config.py             # Settings (env vars, thresholds)
│   │   ├── database.py           # DB engine & session factory
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── dam.py
│   │   │   ├── sensor.py
│   │   │   ├── cooperative.py
│   │   │   ├── user.py
│   │   │   ├── release_order.py
│   │   │   ├── contract.py
│   │   │   ├── forecast.py
│   │   │   └── audit_log.py
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── api/v1/routes/        # All HTTP route handlers
│   │   │   ├── auth.py
│   │   │   ├── dam.py
│   │   │   ├── sensors.py
│   │   │   ├── cooperatives.py
│   │   │   ├── release_orders.py
│   │   │   ├── forecast.py
│   │   │   └── admin.py
│   │   ├── core/
│   │   │   ├── auth.py           # JWT creation & validation
│   │   │   ├── rbac.py           # Role-based access control
│   │   │   └── security.py       # Password hashing, MFA
│   │   ├── services/
│   │   │   ├── dam_service.py    # Safety lock, zone logic
│   │   │   ├── allocation_service.py  # Fair-share formula
│   │   │   ├── sensor_service.py
│   │   │   └── audit_service.py  # Immutable audit trail writer
│   │   └── ml/
│   │       ├── forecast.py       # LSTM + SARIMA water level forecast
│   │       ├── anomaly.py        # Isolation Forest + LSTM Autoencoder
│   │       ├── drought_scorer.py # DSI composite score (0–1)
│   │       └── optimizer.py      # NSGA-II allocation optimization
│   ├── migrations/               # Alembic migration files
│   ├── tests/
│   │   ├── unit/                 # Unit tests per module
│   │   └── integration/          # End-to-end flow tests
│   ├── seed_data.py              # Dev database seeding
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/           # Navbar, Sidebar, ZoneBadge, etc.
│   │   │   ├── dashboard/        # WaterLevelChart, ForecastChart, StatsCard
│   │   │   ├── alerts/           # AlertBanner, AlertList
│   │   │   └── forms/            # ReleaseOrderForm, MFAModal
│   │   ├── pages/                # Dashboard, Orders, Forecast, Admin, Login
│   │   ├── store/                # Zustand global state slices
│   │   ├── services/             # Axios API client wrappers
│   │   ├── hooks/                # useAuth, useDamStatus, useAlerts
│   │   └── utils/                # formatters, zone helpers, constants
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml            # Full local dev stack
├── docker-compose.prod.yml       # Production overrides
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (recommended)
- Or: Python 3.11+, Node.js 20+, PostgreSQL 15+

### Quickstart (Docker — recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_ORG/barrage-flow-manager.git
cd barrage-flow-manager

# 2. Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Start all services
docker compose up --build

# 4. Seed the development database
docker compose exec backend python seed_data.py
```

The app will be available at:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (Redoc):** http://localhost:8000/redoc

### Local Development (without Docker)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env
alembic upgrade head
python seed_data.py
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SECRET_KEY` | JWT signing secret (change in prod!) | — |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiry | `15` |
| `MFA_ISSUER` | TOTP issuer name | `BarrageFlowManager` |
| `SAFETY_RESERVE_THRESHOLD_PCT` | Default critical threshold % | `25.0` |
| `ALERT_ZONE_PCT` | Alert zone lower bound % | `40.0` |
| `WARNING_ZONE_PCT` | Warning zone lower bound % | `25.0` |
| `SMTP_HOST` | Email server for alerts | — |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_BASE_URL` | Backend API base URL |
| `VITE_WS_URL` | WebSocket URL for live sensor data |

---

## Running with Docker

```bash
# Development (with hot reload)
docker compose up

# Run backend tests
docker compose exec backend pytest tests/ -v

# Run database migrations
docker compose exec backend alembic upgrade head

# Open a backend shell
docker compose exec backend bash

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Stop everything
docker compose down

# Stop and remove volumes (reset DB)
docker compose down -v
```

---

## API Documentation

Full interactive docs are auto-generated by FastAPI:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| `POST` | `/api/v1/auth/login` | Login, receive JWT | All |
| `GET` | `/api/v1/dam/status` | Live dam status + zone | All (except Admin) |
| `GET` | `/api/v1/dam/forecast` | 6-month AI forecast | All (except Admin) |
| `GET` | `/api/v1/sensors/` | List all sensors | Director, Operator |
| `POST` | `/api/v1/sensors/readings` | Ingest sensor reading | System / Operator |
| `GET` | `/api/v1/cooperatives/` | List cooperatives + quotas | Director, Operator, Officer |
| `POST` | `/api/v1/release-orders/` | Submit release order | Director, Operator |
| `PATCH` | `/api/v1/release-orders/{id}/approve` | Approve order | Director only |
| `POST` | `/api/v1/release-orders/{id}/override` | Override safety lock | Director + MFA |
| `GET` | `/api/v1/audit-logs/` | View audit trail | Director, Admin |
| `POST` | `/api/v1/admin/users` | Create user account | Admin only |

---

## User Roles

| Role | Description |
|------|-------------|
| **Director** | Full access. Approves orders. Can override safety lock (MFA required). |
| **Operator** | Monitors live data. Submits release orders. Cannot override safety lock. |
| **Agricultural Officer** | Views allocations and cooperative quotas. Submits irrigation requests. |
| **Admin** | Manages user accounts and system health only. Zero access to water data. |

---

## Business Rules

> ⚠️ These are non-negotiable. Every developer must implement them correctly.

1. **Safety Lock** — All releases are auto-blocked when dam level < Safety Reserve Threshold.
2. **Fair Share Formula** — Water is distributed using: `Priority Weight × Contract Share × Available Volume` (weights: A=1.5, B=1.0, C=0.6).
3. **Drought Alert Escalation** — System automatically reduces allocations and changes allowed actions per zone (Normal/Alert/Warning/Critical).
4. **Immutable Audit Trail** — Every significant action is logged permanently. Records can never be edited or deleted.
5. **AI Recommends, Human Decides** — The AI provides recommendations only. A human always makes the final call, and their decision is logged.

---

## Team Modules

| Module | Owner | Status |
|--------|-------|--------|
| Database & Models | — | 🔲 Not started |
| Auth & RBAC | — | 🔲 Not started |
| Sensor Ingestion | — | 🔲 Not started |
| Business Logic | — | 🔲 Not started |
| AI / ML Engine | — | 🔲 Not started |
| REST API Layer | — | 🔲 Not started |
| Frontend Dashboard | — | 🔲 Not started |
| Testing Suite | — | 🔲 Not started |

> Update this table as modules are assigned and completed.

---

## Contributing

1. **Read the team guide** (`docs/Team_Guide.md`) before writing any code.
2. Create a branch: `git checkout -b feature/your-module-name`
3. Follow the module dependency order — **start with Database & Models**.
4. Never hard-code thresholds — they must be configurable in the database.
5. Every function that changes water data **must** write to the AuditLog.
6. Test as every role — Director, Operator, Officer, Admin.
7. Open a PR and request review from your team lead.

---

*Questions? Read the team guide first. Then ask.*
