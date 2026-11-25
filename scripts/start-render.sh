#!/bin/sh
set -eu

# Neon supplies a standard PostgreSQL URL. Select the installed psycopg 3 driver.
case "${DATABASE_URL:?Set the Neon connection string in Render}" in
    postgresql://*) DATABASE_URL="postgresql+psycopg://${DATABASE_URL#postgresql://}" ;;
    postgresql+psycopg://*) ;;
    *) echo 'Expected a PostgreSQL connection string.' >&2; exit 1 ;;
esac
export DATABASE_URL
export PUBLIC_ORIGIN="${PUBLIC_ORIGIN:-${RENDER_EXTERNAL_URL:?Missing public service URL}}"
export BUILD_ID="${RENDER_GIT_COMMIT:-unknown}"
export APP_VERSION="${APP_VERSION:-$BUILD_ID}"

alembic upgrade head
exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-10000}" --no-access-log --no-proxy-headers
