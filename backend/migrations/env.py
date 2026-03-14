"""
Alembic migrations environment.
Reads DATABASE_URL from app settings so we never hardcode credentials.
"""

import sys
from pathlib import Path

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ── Make sure 'app' package is importable ───────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import settings          # noqa: E402
from app.database import Base            # noqa: E402

# ── Import ALL models so Base.metadata knows every table ────────────
# Uncomment each line as you implement the corresponding model:
# from app.models.dam import Dam                        # noqa: E402, F401
# from app.models.sensor import Sensor                  # noqa: E402, F401
# from app.models.cooperative import Cooperative        # noqa: E402, F401
# from app.models.user import User                      # noqa: E402, F401
# from app.models.release_order import ReleaseOrder     # noqa: E402, F401
# from app.models.contract import Contract              # noqa: E402, F401
# from app.models.forecast import Forecast              # noqa: E402, F401
# from app.models.audit_log import AuditLog             # noqa: E402, F401

# ── Alembic Config ──────────────────────────────────────────────────
config = context.config

# Override sqlalchemy.url from env var (never hardcode in alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ── Offline migrations (generate SQL without connecting) ────────────
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online migrations (connect and apply) ───────────────────────────
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
