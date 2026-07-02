"""Entry point: reboot the FritzBox, then exit."""

import logging
import logging.handlers
import os
import sys

from config import LOG_BACKUP_COUNT, LOG_DIR, LOG_FILE, LOG_MAX_BYTES
from rebooter import reboot_fritzbox


def _setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])


def main() -> None:
    _setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("fritzbox-rebooter starting …")

    try:
        reboot_fritzbox()
        logger.info("fritzbox-rebooter finished successfully.")
    except Exception:
        logger.exception("Unhandled error — exiting with code 1.")
        sys.exit(1)


if __name__ == "__main__":
    main()
