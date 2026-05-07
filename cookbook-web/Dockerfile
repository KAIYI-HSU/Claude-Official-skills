# syntax=docker/dockerfile:1.7

# ───────────── Stage 1: build frontend ─────────────
FROM node:20-bookworm-slim AS frontend
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN --mount=type=cache,target=/root/.npm npm install --no-audit --no-fund
COPY frontend/ ./
RUN npm run build


# ───────────── Stage 2: prefetch embedding model ─────────────
FROM python:3.11-slim AS modelprefetch
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
RUN pip install --no-cache-dir sentence-transformers==3.3.1
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('intfloat/multilingual-e5-small', cache_folder='/models')"


# ───────────── Stage 3: runtime ─────────────
FROM python:3.11-slim AS runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    SENTENCE_TRANSFORMERS_HOME=/app/models

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend/app ./app

# Copy built frontend
COPY --from=frontend /build/dist ./frontend/dist

# Copy pre-fetched embedding model
COPY --from=modelprefetch /models ./models

# Cookbooks expected at /app/cookbooks (mount at runtime)
RUN mkdir -p /app/cookbooks /data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s \
  CMD curl -fsS http://localhost:8000/api/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
