recipe-box-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   ├── services/
│   ├── routes/
│   └── middleware.py
├── instance/
│   └── recipes.db
├── wsgi.py
├── .env
├── .env.example
├── requirements.txt
└── REFACTOR_PLAN.md


## Target layout (by feature/layer)

- `app/routes/recipes.py`: HTTP endpoints for recipe CRUD
- `app/routes/auth.py`: HTTP endpoints for register/login
- `app/services/recipes.py`: business logic for recipe CRUD
- `app/services/auth.py`: business logic for auth, tokens, passwords

## Acceptance list (public contract)

1. GET /recipes - returns list of recipes for the current user - 200
2. POST /recipes - creates a recipe with given fields - 201, 400 on bad data
3. PATCH /recipes/<id> - updates an existing recipe if owner/admin - 200, 400, 403, 404
4. DELETE /recipes/<id> - deletes recipe if owner/admin - 204, 403, 404
5. POST /auth/register - creates new user - 201, 400 on bad data
6. POST /auth/login - returns JWT on valid credentials - 200, 401 on bad creds
...


## Responsibility inventory (app.py)

- 8 distinct responsibilities
- List:
  1. creating the Flask app
  2. config / secret key
  3. DB connection / table creation
  4. auth (JWT,password hashing, before_request checks)
  5. recipe CRUD logic
  6. user register/login logic
  7. error handling
  8. starting the server( app.run() )


## Counts

- Responsibilities in app.py: 8
- Acceptance list items: 6