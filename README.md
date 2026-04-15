# Screener.AI – README

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **PostgreSQL** (for full DB features) or run backend in mock-only mode
- Modern web browser

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# (Optional) Create a .env file for custom config
# cp .env.example .env

# Run the Flask development server
python app.py
```

The server starts at **http://localhost:5000**

### 2. Database Setup (Optional – for full DB features)

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE screener_ai;"

# Run schema
psql -U postgres -d screener_ai -f database/schema.sql

# Load seed data
psql -U postgres -d screener_ai -f database/seed_data.sql
```

### 3. Access the App

Open **http://localhost:5000** in your browser.

| Page | URL |
|------|-----|
| Home (Landing) | http://localhost:5000/ |
| Login | http://localhost:5000/pages/login.html |
| Sign Up | http://localhost:5000/pages/signup.html |
| Dashboard | http://localhost:5000/pages/dashboard.html |
| Screeners | http://localhost:5000/pages/screeners.html |
| Sectors | http://localhost:5000/pages/sectors.html |
| Calculators | http://localhost:5000/pages/calculators.html |
| Admin | http://localhost:5000/pages/admin.html |
| Profile | http://localhost:5000/pages/profile.html |

### 4. Seed User Credentials

| Email | Password | Role |
|-------|----------|------|
| admin@screener.ai | Password@123 | Admin |
| rahul@example.com | Password@123 | User |
| priya@example.com | Password@123 | User |

> **Note:** The password hashes in seed_data.sql are placeholder values. Re-register users through the app for real bcrypt hashes.

---

## 🔧 Configuration

All configuration is via environment variables or a `.env` file in the `backend/` folder:

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | PostgreSQL host |
| `DB_NAME` | screener_ai | Database name |
| `DB_USER` | postgres | DB username |
| `DB_PASSWORD` | postgres | DB password |
| `JWT_SECRET` | jwt-dev-secret-change-me | JWT signing key |
| `EMAIL_BACKEND` | fake | `fake` (console) or `smtp` |
| `DATA_PROVIDER` | mock | `mock` or plug in real API |
| `LLM_PROVIDER` | stub | `stub` or `openai`/`anthropic` |
| `LLM_API_KEY` | | Your LLM API key |

### Plugging in Real APIs

1. **Financial Data**: Edit `backend/services/data_provider_service.py` → implement `RealDataProvider` using httpx
2. **LLM Chatbot**: Edit `backend/services/chatbot_service.py` → implement `RealChatbotService` calling your LLM API
3. **Email**: Set `EMAIL_BACKEND=smtp` and configure SMTP variables

---

## 📁 Project Structure

```
project_root/
├── backend/
│   ├── app.py                  # Flask entrypoint
│   ├── config.py               # Configuration
│   ├── requirements.txt
│   ├── models/                 # Data access layer
│   │   ├── user.py
│   │   ├── instrument.py
│   │   ├── screener.py
│   │   ├── portfolio.py
│   │   └── chat.py
│   ├── routes/                 # REST API endpoints
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── instrument_routes.py
│   │   ├── screener_routes.py
│   │   ├── sector_routes.py
│   │   ├── chat_routes.py
│   │   ├── watchlist_routes.py
│   │   └── admin_routes.py
│   └── services/               # Business logic & integrations
│       ├── email_service.py
│       ├── data_provider_service.py
│       ├── chatbot_service.py
│       └── screener_service.py
├── frontend/
│   ├── pages/                  # HTML pages
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   ├── instrument_detail.html
│   │   ├── screeners.html
│   │   ├── sectors.html
│   │   ├── calculators.html
│   │   ├── admin.html
│   │   └── profile.html
│   └── static/
│       ├── css/                # Stylesheets
│       │   ├── base.css
│       │   ├── layout.css
│       │   ├── dashboard.css
│       │   ├── detail.css
│       │   ├── calculators.css
│       │   └── screeners.css
│       └── js/                 # Client-side JavaScript
│           ├── main.js
│           ├── auth.js
│           ├── dashboard.js
│           ├── detail.js
│           ├── screeners.js
│           ├── sectors.js
│           ├── calculators.js
│           ├── chatbot.js
│           └── admin.js
├── database/
│   ├── schema.sql
│   └── seed_data.sql
├── docs/
│   ├── srs.md
│   └── api_reference.md
└── README.md
```

---

## 🎨 Design

Color palette: **Tropical Sunrise**
- `#FF9F1C` – Primary Orange
- `#FFBF69` – Light Peach
- `#FFFFFF` – White
- `#CBF3F0` – Light Mint
- `#2EC4B6` – Teal

Font: **Inter** (Google Fonts)  
Charts: **Chart.js** (CDN)  
Theme: Light/Dark toggle supported
