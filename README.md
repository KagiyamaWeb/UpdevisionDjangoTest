# Django/DRF Auth Backend

Minimal JWT auth backend with a custom user model that supports email or phone as identifiers. Uses DRF + SimpleJWT and a middleware that rotates access tokens on each authenticated request.

## Key Features
- Custom `User` (email/phone, no username)
- JWT access tokens (5 min)
- Auto-rotate access token via `X-New-Access-Token` response header

## Endpoints (under `/api/`)
- POST `/signup/` – create user (email or phone) and return access token
- POST `/signin/` – login with email or phone, return access token
- GET `/info/` – returns `id` and `id_type` of current user
- GET `/latency/` – demo endpoint that measures a request to `https://ya.ru`

## Auth Model & Flow
- `auth_api.models.User` extends `AbstractUser`, disables `username`, supports `email` or `phone` (unique, optional). `USERNAME_FIELD = 'email'` but signin accepts either via view logic.
- Short-lived access tokens only. No refresh tokens are issued.
- Middleware (`AutoRefreshJWTMiddleware`) adds `X-New-Access-Token` header on successful authenticated responses (excluding `/api/signin/` and `/api/signup/`). Clients should replace the token they hold with this header value.

## Quickstart
1) Create venv and install deps
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
2) Migrate and run
```bash
python manage.py migrate
python manage.py runserver
```
3) Try it
```bash
# Sign up
curl -sS -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"id_type":"email","email":"user@example.com","password":"pass12345"}'

# Sign in
curl -sS -X POST http://localhost:8000/api/signin/ \
  -H "Content-Type: application/json" \
  -d '{"id":"user@example.com","password":"pass12345"}'

# Authenticated call (observe X-New-Access-Token)
curl -i http://localhost:8000/api/info/ -H "Authorization: Bearer <access>"
```

## Configuration Highlights
- `AUTH_USER_MODEL = 'auth_api.User'`
- DRF: `JWTAuthentication` + global `IsAuthenticated`
- SimpleJWT: `ACCESS_TOKEN_LIFETIME = 5 minutes`
- Middleware: `auth_api.middleware.AutoRefreshJWTMiddleware`

## Files of Interest
- `auth_api/models.py` – `User`, `UserManager`
- `auth_api/serializers.py` – registration/login serializers
- `auth_api/views.py` – endpoints (now with proper permissions)
- `auth_api/middleware.py` – token rotation header
- `core/settings.py` – DRF/JWT, custom user, global permissions
