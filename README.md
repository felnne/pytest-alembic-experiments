# Pytest-Alembic Experiments

Setup:

```
$ poetry install
$ echo '/Users/felnne/Projects/_scratch/2023/pytest-alembic-exp/src' > .venv/lib/python3.8/site-packages/coke.pth
$ psql -d postgres -c 'CREATE DATABASE pytest_alembic;'
```

Check things work manually:

```
$ poetry run alembic upgrade head
$ SQLALCHEMY_SILENCE_UBER_WARNING=1 poetry run python -m coke
$ poetry run alembic downgrade base
```

Reset DB:

```
$ psql -d postgres -c 'DROP DATABASE IF EXISTS pytest_alembic;' && psql -d postgres -c 'CREATE DATABASE pytest_alembic;'
```

Run tests:

```
$ SQLALCHEMY_SILENCE_UBER_WARNING=1 poetry run pytest
```

## Notes:

* once DSN removed from `alembic.ini`, all other config options are either static (package location) or defaults

If DDL test fails, you can generate an automatic migration to see what's missing:

```
$ poetry run alembic upgrade head
$ poetry run alembic revision --autogenerate
```

If SQLAlchemy models are not as up to date as the Alembic models, the upgrade/downgrade steps will be flipped around.

## TODO:

DSN is defined twice in:

* `alembic.ini`
* `tests/conftest.py`
* `src/pytest_alembic_exp/main.py`
