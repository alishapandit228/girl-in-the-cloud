"""Create private analytics, contact receipts and owner sessions."""
from alembic import op
revision="001"
down_revision=None
def upgrade():
    op.execute("CREATE TABLE sessions (token TEXT PRIMARY KEY, expires BIGINT NOT NULL)")
    op.execute("CREATE TABLE limits (bucket TEXT PRIMARY KEY, hits INTEGER NOT NULL, expires BIGINT NOT NULL)")
    op.execute("CREATE TABLE events (day TEXT NOT NULL, visitor TEXT NOT NULL, kind TEXT NOT NULL, path TEXT NOT NULL, device TEXT NOT NULL, referrer TEXT NOT NULL)")
    op.execute("CREATE INDEX events_day ON events(day)")
    op.execute("CREATE TABLE contacts (id TEXT PRIMARY KEY, created BIGINT NOT NULL, state TEXT NOT NULL)")
def downgrade():
    for table in ("contacts","events","limits","sessions"):
        op.drop_table(table)
