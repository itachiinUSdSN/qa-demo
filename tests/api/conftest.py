import os

import httpx
import pytest


@pytest.fixture
def client():
    # No default URL on purpose: a test must never silently hit the wrong server.
    with httpx.Client(base_url=os.environ["STAGING_URL"], timeout=30) as c:
        yield c
