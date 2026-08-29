FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SCORESYMPHONY_STATE_DIR=/var/lib/scoresymphony-agent

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-cache-dir .

RUN useradd --create-home --system scoresymphony-agent \
    && mkdir -p /var/lib/scoresymphony-agent \
    && chown -R scoresymphony-agent:scoresymphony-agent /var/lib/scoresymphony-agent

USER scoresymphony-agent
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3)" || exit 1

ENTRYPOINT ["scoresymphony-agent"]
CMD ["serve"]
