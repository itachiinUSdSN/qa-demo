"""Starts the throwaway plants app (plants/app.py) on a free localhost port for the tests in this folder."""
import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from plants.app import serve  # noqa: E402


@pytest.fixture(scope="session")
def plants_url():
    server = serve(0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()
