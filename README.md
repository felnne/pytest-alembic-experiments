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
$ poetry run alembic downgrade base
```

Reset DB:

```
$ psql -d postgres -c 'DROP DATABASE IF EXISTS pytest_alembic;' && psql -d postgres -c 'CREATE DATABASE pytest_alembic;'
```

Run tests:

```
$ poetry run pytest
```

## Notes:

* once DSN removed from `alembic.ini`, all other config options are either static (package location) or defaults

## TODO:

DSN is defined twice in:

* `alembic.ini`
* `tests/conftest.py`
