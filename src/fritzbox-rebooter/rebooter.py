"""Triggers a FritzBox reboot via the TR-064 DeviceConfig SOAP action."""

import logging

import requests
from requests.auth import HTTPDigestAuth

from config import (
    FRITZBOX_HOST,
    FRITZBOX_PASSWORD,
    FRITZBOX_PORT,
    FRITZBOX_USER,
    REQUEST_TIMEOUT,
    SOAP_ACTION,
    SOAP_LOCATION,
    SOAP_URI,
)

logger = logging.getLogger(__name__)

SOAP_BODY = (
    "<?xml version='1.0' encoding='utf-8'?>"
    "<s:Envelope s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/' "
    "xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'>"
    "<s:Body>"
    f"<u:{SOAP_ACTION} xmlns:u='{SOAP_URI}'></u:{SOAP_ACTION}>"
    "</s:Body>"
    "</s:Envelope>"
)


def reboot_fritzbox() -> None:
    """Sends the TR-064 reboot command to the configured FritzBox.

    Raises:
        RuntimeError: if credentials are missing.
        requests.RequestException: if the request fails or FritzBox returns an error status.
    """
    if not FRITZBOX_USER or not FRITZBOX_PASSWORD:
        raise RuntimeError(
            "FRITZBOX_USER and FRITZBOX_PASSWORD must be set via environment variables."
        )

    url = f"http://{FRITZBOX_HOST}:{FRITZBOX_PORT}{SOAP_LOCATION}"
    headers = {
        "Content-Type": 'text/xml; charset="utf-8"',
        "SoapAction": f"{SOAP_URI}#{SOAP_ACTION}",
    }

    logger.info("Sending reboot command to FritzBox at %s", FRITZBOX_HOST)
    response = requests.post(
        url,
        headers=headers,
        data=SOAP_BODY,
        auth=HTTPDigestAuth(FRITZBOX_USER, FRITZBOX_PASSWORD),
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    logger.info("FritzBox accepted the reboot command (HTTP %d).", response.status_code)
