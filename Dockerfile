FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.2.1 poetry-plugin-export==1.10.0

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes --only main -f requirements.txt -o requirements.txt


FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/fritzbox-rebooter/ ./

# Runs once and exits — no cron, no scheduler, no ENTRYPOINT loop.
# Triggering (Portainer, Proxmox host cron, systemd timer, ...) happens outside the container.
CMD ["python", "main.py"]
