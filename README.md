# Pytest-Alembic Experiments

Setup:

```
$ poetry install
$ echo '/Users/felnne/Projects/_scratch/2023/pytest-alembic-exp/src' > .venv/lib/python3.8/site-packages/coke.pth
$ psql -d postgres -c 'CREATE DATABASE pytest_alembic;'
```

Check things work manually:

```
$ APP_DB_DSN=postgresql://felnne@localhost/pytest_alembic poetry run alembic upgrade head
$ SQLALCHEMY_SILENCE_UBER_WARNING=1 APP_DB_DSN=postgresql://felnne@localhost/pytest_alembic poetry run python -m coke
$ APP_DB_DSN=postgresql://felnne@localhost/pytest_alembic poetry run alembic downgrade base
```

Reset DB:

```
$ psql -d postgres -c 'DROP DATABASE IF EXISTS pytest_alembic;' && psql -d postgres -c 'CREATE DATABASE pytest_alembic;'
```

Check DB DSN environment variable set correctly:

```
$ APP_DB_DSN=postgresql://felnne@localhost/pytest_alembic poetry run python -m coke.config
```

Run tests:

```
$ APP_DB_DSN=postgresql://felnne@localhost/pytest_alembic SQLALCHEMY_SILENCE_UBER_WARNING=1 poetry run pytest
```

## Notes:

* once DSN removed from `alembic.ini`, all other config options are either static (package location) or defaults
* offline mode is where Alembic generates SQL statements to run standalone, rather than Alembic modifying the DB
* if DDL test fails, you can generate an automatic migration to see what's missing [1]
* in CI, Alembic fails because the official PostGIS image includes more than just the PostGIS extension (tiger etc.)
  * rather than create a new image etc. it may be easiest to add `psql` in the app container and drop extra extensions?
  * see https://github.com/postgis/docker-postgis/issues/187 for changing image to not add these extensions by default

[1]

```
$ poetry run alembic upgrade head
$ poetry run alembic revision --autogenerate
```

If SQLAlchemy models are not as up to date as the Alembic models, the upgrade/downgrade steps will be flipped around.

## TODO:

- [x]  SQLAlchemy tests
- [x]  Does the rolled back in the DB fixture mean we don't need migrations to be run, as it doesn't touch the DB?
    - no, committing the session actually modifies the DB
- [x]  what is 'offline mode' in Alembic?
  - where Alembic generates SQL to run externally 
- [x]  DSN is defined multiple times [1]
- [ ]  GitLab CI

Next:

- [ ]  More realistic tests (i.e. from locations register)
- [ ]  Pytest-alembic experimental tests

[1]

* ~~`alembic.ini`~~
* `src/pytest_alembic_exp/db.py`
