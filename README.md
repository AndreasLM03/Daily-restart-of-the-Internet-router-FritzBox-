# FritzBox Rebooter

Everyone is annoyed by the fact that every now and then the Internet stops working properly. The usual fix is a simple reboot of the router. This is a lightweight Docker container that automatically reboots a FritzBox via its TR-064 SOAP interface — no browser, no Selenium, plain HTTP only. Scheduled to run daily, it guarantees a good and stable connection (great for HomeOffice).

---

## How it works

The container starts, sends the TR-064 `Reboot` SOAP action to the FritzBox, logs the result, and exits. Scheduling is handled outside the container (cron / systemd / Portainer).

---

## FritzBox setup

Create a dedicated username and password in the FritzBox interface (Home Network → Network → Network Settings → FRITZ!Box Users) with permission for "FRITZ!Box Settings". Never reuse your main admin login for this.

<img src="images/01 fritzbox.jpg" width="800">
<img src="images/02 fritzbox.jpg" width="800">

---

## Project structure

```
fritzbox-rebooter/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml / poetry.lock
├── .env.example
├── src/fritzbox-rebooter/
│   ├── config.py     # env-based configuration (host, credentials, paths)
│   ├── rebooter.py   # TR-064 SOAP reboot call
│   └── main.py        # entry point + logging setup
└── tests/
```

**Logs** (`/data/logs/fritzbox-rebooter.log`, rotated at 1 MB × 3 backups):
```
2026-07-02 06:00:01 INFO __main__ fritzbox-rebooter starting …
2026-07-02 06:00:01 INFO rebooter Sending reboot command to FritzBox at 192.168.178.1
2026-07-02 06:00:02 INFO rebooter FritzBox accepted the reboot command (HTTP 200).
2026-07-02 06:00:02 INFO __main__ fritzbox-rebooter finished successfully.
```

---

## Configuration

All settings are passed as environment variables — no credentials are ever hardcoded or committed.

| Variable | Required | Default | Description |
|---|---|---|---|
| `FRITZBOX_HOST` | no | `192.168.178.1` | IP address of the FritzBox |
| `FRITZBOX_PORT` | no | `49000` | TR-064 SOAP port |
| `FRITZBOX_USER` | **yes** | — | FritzBox user with settings permission |
| `FRITZBOX_PASSWORD` | **yes** | — | Password for that user |
| `REQUEST_TIMEOUT` | no | `10` | HTTP timeout in seconds |
| `DATA_DIR` | no | `/data` | Where logs are written (mounted volume) |
| `TZ` | no | — | Timezone for log timestamps |

Copy `.env.example` to `.env` and fill in your values (`.env` is gitignored, never commit it).

---

## Run locally

```bash
cp .env.example .env   # fill in FRITZBOX_USER / FRITZBOX_PASSWORD

mkdir -p ~/fritzbox-rebooter-data/logs

docker build -t fritzbox-rebooter:latest .

docker run --rm \
  -v ~/fritzbox-rebooter-data:/data \
  --env-file .env \
  fritzbox-rebooter:latest
```

Or with Compose:

```bash
docker compose --env-file .env up --build
```

---

## Deploy on Proxmox / Portainer

Pull the image directly from GitHub Container Registry:

```
ghcr.io/YOUR_GITHUB_USERNAME/fritzbox-rebooter:latest
```

**Portainer → Add container:**

| Field | Value |
|---|---|
| Image | `ghcr.io/YOUR_GITHUB_USERNAME/fritzbox-rebooter:latest` |
| Restart policy | Never |
| Volume | `/opt/fritzbox-rebooter-data` → `/data` (bind mount) |
| Env | `FRITZBOX_HOST`, `FRITZBOX_USER`, `FRITZBOX_PASSWORD`, `TZ=Europe/Berlin` |

**Daily scheduling on the host** (e.g. a Raspberry Pi or the Proxmox host itself):

```bash
# crontab -e
0 6 * * * docker run --rm -v /opt/fritzbox-rebooter-data:/data --env-file /opt/fritzbox-rebooter-data/.env ghcr.io/YOUR_GITHUB_USERNAME/fritzbox-rebooter:latest
```

This restarts the router every day at 6 am.