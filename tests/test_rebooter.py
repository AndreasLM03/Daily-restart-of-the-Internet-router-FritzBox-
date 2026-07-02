"""Tests for rebooter.py — run with: pytest tests/"""

import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "fritzbox-rebooter"))


@pytest.fixture()
def env(monkeypatch):
    monkeypatch.setenv("FRITZBOX_HOST", "192.168.178.1")
    monkeypatch.setenv("FRITZBOX_USER", "testuser")
    monkeypatch.setenv("FRITZBOX_PASSWORD", "testpass")
    for mod in ["config", "rebooter"]:
        if mod in sys.modules:
            del sys.modules[mod]


def test_reboot_fritzbox_sends_soap_request(env):
    import rebooter

    with patch("rebooter.requests.post") as mock_post:
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.status_code = 200

        rebooter.reboot_fritzbox()

        assert mock_post.call_count == 1
        _, kwargs = mock_post.call_args
        assert "192.168.178.1:49000" in mock_post.call_args.args[0]
        assert "Reboot" in kwargs["headers"]["SoapAction"]


def test_reboot_fritzbox_raises_without_credentials(monkeypatch):
    monkeypatch.delenv("FRITZBOX_USER", raising=False)
    monkeypatch.delenv("FRITZBOX_PASSWORD", raising=False)
    for mod in ["config", "rebooter"]:
        if mod in sys.modules:
            del sys.modules[mod]
    import rebooter

    with pytest.raises(RuntimeError):
        rebooter.reboot_fritzbox()
