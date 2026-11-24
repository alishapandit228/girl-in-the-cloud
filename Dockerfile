FROM node:22-bookworm-slim AS ui
WORKDIR /build/frontend
COPY frontend/package*.json ./
RUN npm install --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv/app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --system --uid 10001 portfolio
COPY backend backend
COPY content content
COPY frontend/public frontend/public
COPY frontend/templates frontend/templates
COPY --from=ui /build/frontend/public/enhanced frontend/public/enhanced
COPY scripts scripts
COPY alembic.ini .
RUN python scripts/social.py
USER portfolio
EXPOSE 8000
CMD ["sh","-ec","alembic upgrade head && exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --no-access-log --forwarded-allow-ips=172.29.44.3"]
