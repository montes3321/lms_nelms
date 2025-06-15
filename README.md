# lms_nelms
attempt for create lms

## Database Setup

Alembic migrations are stored in the `alembic` folder. To initialize the test SQLite database and apply migrations run:

```bash
alembic upgrade head
```

To seed base roles run:

```bash
python seed_roles.py
```

Application settings such as token lifetime and secret key can be configured in
the `.env` file. Default values are provided in the repository.

An ER diagram of auth related tables is available in `docs/erd_auth.mmd`.
