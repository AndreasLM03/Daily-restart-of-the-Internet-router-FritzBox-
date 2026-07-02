"""Central configuration for fritzbox-rebooter."""

import os

# Data directory — mounted as Docker volume (logs only, no other state)
DATA_DIR: str = os.getenv("DATA_DIR", "/data")
LOG_DIR: str = os.path.join(DATA_DIR, "logs")
LOG_FILE: str = os.path.join(LOG_DIR, "fritzbox-rebooter.log")

# Logging
LOG_MAX_BYTES: int = 1 * 1024 * 1024  # 1 MB
LOG_BACKUP_COUNT: int = 3

# FritzBox connection — credentials come from the environment, never hardcoded
FRITZBOX_HOST: str = os.getenv("FRITZBOX_HOST", "192.168.178.1")
FRITZBOX_PORT: int = int(os.getenv("FRITZBOX_PORT", "49000"))
FRITZBOX_USER: str | None = os.getenv("FRITZBOX_USER")
FRITZBOX_PASSWORD: str | None = os.getenv("FRITZBOX_PASSWORD")

# HTTP
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

# TR-064 SOAP action for a device reboot
SOAP_LOCATION: str = "/upnp/control/deviceconfig"
SOAP_URI: str = "urn:dslforum-org:service:DeviceConfig:1"
SOAP_ACTION: str = "Reboot"
