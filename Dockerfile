# base image
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ ./src/
COPY config.json ./src/
CMD ["python", "-m", "main"]
