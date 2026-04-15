# Screener.AI – API Reference

## Base URL
```
http://localhost:5000/api
```

All endpoints return JSON. Authenticated endpoints require `Authorization: Bearer <token>` header.

---

## Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Register new user |
| POST | `/auth/verify-otp` | ❌ | Verify email OTP |
| POST | `/auth/login` | ❌ | Login, returns JWT |
| POST | `/auth/resend-otp` | ❌ | Resend OTP |

### POST `/auth/register`
```json
// Request
{ "email": "user@example.com", "password": "SecurePass1!", "name": "John Doe" }
// Response 201
{ "message": "Registration successful...", "user_id": 1, "email": "user@example.com" }
```

### POST `/auth/login`
```json
// Request
{ "email": "user@example.com", "password": "SecurePass1!" }
// Response 200
{ "access_token": "eyJ...", "user": { "id": 1, "email": "...", "name": "...", "role": "user" } }
```

---

## User Profile

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/user/profile` | ✅ | Get current user profile |
| PUT | `/user/profile` | ✅ | Update profile fields |

### PUT `/user/profile`
```json
// Request
{ "name": "Updated", "risk_profile": "Aggressive", "experience_level": "Intermediate", "age": 30 }
```

---

## Instruments

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/instruments/search?q=...` | ❌ | Search by name/symbol |
| GET | `/instruments/{id}` | ❌ | Instrument detail |
| GET | `/instruments/{id}/chart?range=1M` | ❌ | Historical price data |
| GET | `/instruments/{id}/fundamentals` | ❌ | Fundamentals history |

### GET `/instruments/search?q=TCS`
```json
// Response
[{ "id": 1, "symbol": "TCS", "name": "Tata Consultancy Services", "current_price": 3845.50, "day_change_pct": 0.84 }]
```

### Chart ranges: `1D`, `1W`, `1M`, `3M`, `6M`, `1Y`, `5Y`, `MAX`

---

## Watchlists

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/watchlists/` | ✅ | List user watchlists with items |
| POST | `/watchlists/` | ✅ | Create watchlist |
| POST | `/watchlists/{id}/items` | ✅ | Add instrument to watchlist |
| DELETE | `/watchlists/{id}/items/{itemId}` | ✅ | Remove item |

---

## Portfolio

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/portfolio/` | ✅ | List positions with P/L |
| POST | `/portfolio/positions` | ✅ | Add new position |

### POST `/portfolio/positions`
```json
{ "instrument_id": 1, "quantity": 10, "buy_price": 3500.00, "buy_date": "2025-01-15" }
```

---

## Screeners

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/screeners/predefined` | ❌ | List predefined screens |
| GET | `/screeners/custom` | ✅ | List user's saved screens |
| POST | `/screeners/custom` | ✅ | Save custom screen |
| POST | `/screeners/run` | ❌ | Run a screen |

### POST `/screeners/run`
```json
// Request
{ "definition_json": { "conditions": [{ "field": "roe", "op": ">", "value": 15 }, { "field": "debt_to_equity", "op": "<", "value": 0.5 }], "logic": "AND" } }
// Response
[{ "id": 1, "symbol": "TCS", "name": "...", "roe": 48.5, "debt_to_equity": 0.14, ... }]
```

### Available filter fields:
`pe`, `pb`, `roe`, `roce`, `debt_to_equity`, `net_profit_margin`, `sales_growth`, `profit_growth`, `market_cap`

---

## Sectors

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/sectors/` | ❌ | List sectors with stats |
| GET | `/sectors/{name}/instruments` | ❌ | Instruments in sector |

---

## Chat (AI Chatbot)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/chat` | ✅ | Send message to AI chatbot |

### POST `/chat`
```json
// Request
{ "instrumentId": 1, "userMessage": "Is this stock suitable for a beginner?" }
// Response
{ "response": "Based on the fundamentals of TCS..." }
```

---

## Admin

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/admin/users` | ✅ Admin | List all users |
| PUT | `/admin/users/{id}/toggle` | ✅ Admin | Toggle active/disabled |

---

## Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Returns `{ "status": "ok" }` |
