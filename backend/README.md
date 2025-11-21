# Django + MongoDB (mongoengine) backend scaffold for Fast-Food project

## Setup (local)

1. Create and activate virtualenv

```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and edit values.

3. Run server

```
python manage.py runserver 0.0.0.0:8000
```

API endpoints available at: `http://localhost:8000/api/`

- `POST /api/auth/register/` - register {name,email,password}
- `POST /api/auth/login/` - login {email,password}
- `GET /api/foods/` - list foods
- `POST /api/foods/create/` - create food
- `POST /api/upload/` - upload file (multipart/form-data)
- `GET /api/orders/` - list orders
- `POST /api/orders/create/` - create order

Notes:
- This scaffold uses mongoengine (MongoDB) and a simple JWT implementation. It's intended as an MVP starting point. 
- In production, use a robust password hashing scheme (bcrypt), add logging, monitoring, and secure media hosting (S3/Cloud).
