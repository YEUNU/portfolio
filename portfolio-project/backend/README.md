Alembic migrations
------------------

This backend uses Alembic for schema migrations. The repository includes a minimal
Alembic skeleton at `backend/alembic/` and an `alembic.ini` file.

Common commands (run from `portfolio-project/backend`):

- Create a new revision (autogenerate):

  alembic -c alembic.ini revision --autogenerate -m "create initial tables"

- Apply migrations:

  alembic -c alembic.ini upgrade head

- Note: Alembic will use the app configuration to find the database URL. Ensure
  your `../.env` has the correct `DATABASE_URI` or `POSTGRES_*` variables.

Development convenience
- To let the app create tables automatically on startup (only for dev), set
  `INIT_DB=true` in your `.env` file. In production, prefer Alembic migrations
  and keep `INIT_DB=false`.
