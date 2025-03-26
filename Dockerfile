FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Disable Python downloads, because we want to use the system interpreter
# across both images. If using a managed Python version, it needs to be
# copied from the build image into the final image; see `standalone.Dockerfile`
# for an example.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-dev
COPY pyproject.toml uv.lock .python-version README.md ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

# Then, use a final image without uv
FROM python:3.13-slim-bookworm
ENV TINI_VERSION=v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

WORKDIR /app

COPY ./scripts ./scripts

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Prefetch models
RUN python ./scripts/prefetch_models.py

EXPOSE 8000
# Run the FastAPI application by default
ENTRYPOINT ["/tini", "--"]
CMD ["uvicorn", "--factory", "src.bm25_inference.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
