from logging.config import fileConfig
from pathlib import Path

from alembic import context
from importlib_resources import as_file as resource_path_as_file, files as resource_path

from coke.config import db_dsn
from coke.db import Base as MetadataBase

# Load base Alembic config
config = context.config

# Set SQLAlchemy metadata instance, used for 'autogenerate' support
target_metadata = MetadataBase.metadata


def get_alembic_logging_path() -> Path:
    """Generate path to logging config file from within application package."""
    with resource_path_as_file(resource_path("coke.alembic")) as alembic_path:
        return Path(alembic_path).joinpath('logging.ini')


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    In this mode Alembic generates SQL statements to be run elsewhere (i.e. by an external DBA). SQL that would be
    normally be executed against the DB is emitted as script output.

    Alembic's context is configured with a URL, rather than an Engine, which doesn't require the DB to be accessible.
    """
    context.configure(
        url=db_dsn,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this mode Alembic executes SQL statements against the DB directly

    Alembic's context is configured with an Engine and an associated DB connection to do this.
    """
    connectable = context.config.attributes.get("connection", None)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Setup Alembic logging from application package
fileConfig(fname=get_alembic_logging_path(), disable_existing_loggers=False)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


# other values from the config, defined by the needs of env.py, can be acquired:
# e.g. `my_important_option = config.get_main_option("my_important_option")`
