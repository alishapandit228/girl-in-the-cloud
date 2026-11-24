import os
from alembic import context
from sqlalchemy import create_engine
with create_engine(os.environ["DATABASE_URL"]).connect() as conn:
    context.configure(connection=conn)
    with context.begin_transaction():
        context.run_migrations()
