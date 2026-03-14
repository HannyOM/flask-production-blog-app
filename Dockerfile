FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml package.json package-lock.json ./
COPY wsgi.py ./
COPY bloggr ./bloggr
COPY migrations ./migrations
COPY tailwind.config.js postcss.config.js ./

RUN pip install --no-cache-dir -e . && \
    npm ci --only=production=false && \
    npm run build-css

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

ENV PORT=8000

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "--workers", "4", "--timeout", "120", "--pythonpath", "/app", "wsgi:app"]
