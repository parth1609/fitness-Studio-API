# Fitness Studio Booking API

FastAPI-based API to manage fitness classes and bookings. It supports user signup/login (JWT), creating/listing classes, and booking classes.

## Project overview
* __Stack__: FastAPI, SQLAlchemy, Pydantic v2, SQLite, JWT (python-jose)
* __Auth__: Email/password, password hashed via Passlib/bcrypt, JWT Bearer tokens
* __Time__: Class times normalized to IST (Asia/Kolkata) and validated as future
* __Build__: Bazel (official). Minimal example provided below.
* __Testing__: pytest + httpx
* __Docs__: Swagger UI at `/docs`

## Source code
```
app/
  main.py                 # FastAPI app, includes routers, creates DB tables on startup
  models.py               # SQLAlchemy models: User, FitnessClass, Booking
  schemas.py              # Pydantic models (v2) with camelCase response aliases
  dependencies.py         # get_db, get_current_user (HTTP Bearer JWT)
  core/
    config.py             # Settings via env vars (SECRET_KEY, DATABASE_URL, etc.)
    jwt.py                # JWT create/decode helpers
    security.py           # Password hashing/verification
  db/
    session.py            # SQLAlchemy engine + session factory
  routers/
    auth.py               # POST /signup, POST /login
    classes.py            # POST /classes, GET /classes
    bookings.py           # POST /book, GET /bookings
  utils/
    time.py               # IST helpers: now_ist, normalize_to_ist, is_past_in_ist
tests/
  test_health.py, test_auth.py, test_classes_bookings.py
requirements.txt
README.md
```

## Setup instructions
1) __Python__ 3.11+ recommended
2) __Create venv__ (Windows PowerShell)
   ```ps1
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
3) __Install deps__
   ```bash
   pip install -r requirements.txt
   ```
4) __Environment (optional)__: create `.env` or export variables before running
   - `SECRET_KEY`: default is a dev value; set a random value in prod
   - `DATABASE_URL`: default `sqlite:///./db.sqlite3`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: default `60`

## How to run locally
### Option A: Bazel (official)
This repo is lightweight and doesn’t ship Bazel files by default. If your team uses Bazel as the official build system, create minimal Bazel targets to run Uvicorn (example snippet):
```python
# BUILD (example)
py_binary(
    name = "serve",
    srcs = ["main.py"],  # consider adding a tiny serve.py that shells out to uvicorn
    deps = [
        # deps for FastAPI app here
    ],
)
# Then: bazel run //app:serve  # ensure the binary invokes `uvicorn app.main:app`
```
For production, prefer a dedicated entrypoint that calls `uvicorn.run(...)`.

### Option B: Uvicorn (quickstart)
```bash
uvicorn app.main:app --reload
```
Visit Swagger: http://127.0.0.1:8000/docs

## Usage (with screenshots)
> Place screenshots in `docs/images/` with the filenames below. On Windows, use Win+Shift+S (Snipping Tool) and save as PNG.

1) __Open Swagger UI__ (`/docs`)

   ![Swagger home](docs/images/swagger-overview.png)

2) __Authorize__ → paste your JWT (raw token, no Bearer prefix)

   ![Authorize button](docs/images/swagger-authorize-button.png)

   ![Paste token](docs/images/swagger-authorize-token.png)



### Windows cURL tips
* PowerShell line continuation uses backtick `, not backslash \
* Replace `<TOKEN>` with the JWT string from `/login`.
* Prefer one-line requests or use `Invoke-RestMethod`:

```ps1
$body = '{"name":"Ana","email":"ana@example.com","password":"secret123"}'
Invoke-RestMethod -Uri "http://127.0.0.1:8000/signup" -Method POST -ContentType "application/json" -Body $body
```

## Sample seed/input data
Use the following sequence to create a user, obtain a token, create a class (future IST), and book it.

### 1) Signup
```bash
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ana",
    "email": "ana@example.com",
    "password": "secret123"
  }'
```

### 2) Login (copy the access_token)
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ana@example.com",
    "password": "secret123"
  }'
```

### 3) Create a class (requires Bearer token)
Pick a future IST datetime, e.g. `2025-09-02T09:00:00+05:30`.
```bash
curl -X POST http://127.0.0.1:8000/classes \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yoga 101",
    "dateTime": "2025-09-02T09:00:00+05:30",
    "instructor": "Ravi",
    "availableSlots": 10
  }'
```

### 4) List upcoming classes
```bash
curl http://127.0.0.1:8000/classes
```

### 5) Book the class (requires Bearer token)
```bash
curl -X POST http://127.0.0.1:8000/book \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "Ana",
    "client_email": "ana@example.com"
  }'
```

### 6) See your bookings
```bash
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/bookings
```

## API usage (Postman)
1) Import a new request for each endpoint above.
2) Add `Authorization: Bearer <TOKEN>` for protected routes (`/classes` POST, `/book`, `/bookings`).
3) Set body type to `raw` JSON.

## Testing
```bash
pytest -q
```

## Troubleshooting
* __401 Not authenticated__: Click "Authorize" in Swagger and paste your JWT (raw token; Swagger adds "Bearer ").
* __400 Past class__: Ensure `dateTime` is in the future IST.
* __Naive/aware datetime__: The app normalizes timestamps to IST before comparing.
