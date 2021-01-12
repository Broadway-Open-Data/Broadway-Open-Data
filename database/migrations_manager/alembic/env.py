import os
import sys
from pathlib import Path
if os.environ.get('PROJECT_PATH'):
    sys.path.append(os.environ.get('PROJECT_PATH'))

# Append the path to the root directory of the project
sys.path.append('/Users/yaakov/Documents/Open Broadway Data/Data-Collection/')
sys.path.append('/Users/nickwilders/Desktop/obd/Data-Collection')


from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Get secrets
import os
DB_URI = os.environ.get('DB_URI', 'mysql+pymysql://root:broadway@localhost:3306/broadway')

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url',DB_URI)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Autodection...
from database import metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.



IGNORE_TABLES = ('',)


def include_symbol(tablename, schema):
    return tablename not in IGNORE_TABLES


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        compare_type=True,
        # include_symbol=include_symbol,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """


    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            # include_symbol=include_symbol,
        )



        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()











#
