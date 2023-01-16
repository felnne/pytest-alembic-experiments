# Pytest Alembic Experiments

Experiments using pytest to validate Alembic database migrations

## Overview

This experiment uses a very simple database model (a single `Foo` entity with an auto-incrementing ID and text label).

It is used to verify:

- a set of [Alembic migrations](https://alembic.sqlalchemy.org) can be tested using [pytest](https://pytest.org) and 
  [pytest-alembic](https://pytest-alembic.readthedocs.io/en/latest/)
- CRUD operations for SQLAlchemy models can be tested

## Setup

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

## Usage

Locally:

```
$ APP_DB_DSN=postgresql://felnne@localhost/pytest_alembic SQLALCHEMY_SILENCE_UBER_WARNING=1 poetry run pytest
```

CI:

- commits to this repository will trigger GitLab CI to run tests using a service container, see `.gitlab-ci.yml`

## Notes

* once DSN removed from `alembic.ini`, all other config options are either static (package location) or defaults
* offline mode is where Alembic generates SQL statements to run standalone, rather than Alembic modifying the DB
* if DDL test fails, you can generate an automatic migration to see what's missing [1]
* in CI, Alembic fails because the official PostGIS image includes more than just the PostGIS extension (tiger etc.)
  * rather than create a new image etc. it was easiest to add `psql` in the app container and drop extra extensions
  * see https://github.com/postgis/docker-postgis/issues/187 for changing image to not add these extensions by default

[1]

```
$ poetry run alembic upgrade head
$ poetry run alembic revision --autogenerate
```

If SQLAlchemy models are not as up to date as the Alembic models, the upgrade/downgrade steps will be flipped around.

## TODO

- [x]  SQLAlchemy tests
- [x]  Does the rolled back in the DB fixture mean we don't need migrations to be run, as it doesn't touch the DB?
    - no, committing the session modifies the DB
- [x]  what is 'offline mode' in Alembic?
  - where Alembic generates SQL to run externally 
- [x]  DSN is defined multiple times [1]
- [x]  GitLab CI

Next:

- [ ]  More realistic tests (i.e. from locations register)
- [ ]  Pytest-alembic [experimental tests](http://pytest-alembic.readthedocs.io/en/latest/experimental_tests.html)

## Licence

Copyright (c) 2023 UK Research and Innovation (UKRI), British Antarctic Survey.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
