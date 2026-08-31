FROM node:22-alpine AS frontend-build
WORKDIR /build
COPY frontend/package.json ./
RUN npm install --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SCORESYMPHONY_ENV=production \
    SCORESYMPHONY_STATE_ROOT=/var/lib/scoresymphony-agent
WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .

COPY --from=frontend-build /build/dist /app/frontend

RUN useradd --system --uid 10001 --create-home --home-dir /home/scoresymphony scoresymphony \
    && mkdir -p /var/lib/scoresymphony-agent \
    && chown -R scoresymphony:scoresymphony /var/lib/scoresymphony-agent /app

USER scoresymphony
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/v1/health', timeout=2).read()"

CMD ["uvicorn", "scoresymphony_agent.app:app", "--host", "0.0.0.0", "--port", "8080"]
