# -*- coding: utf-8 -*-
"""
HTTP request wrapper for API automation testing
Features:
- Auto load config params (timeout, headers, base URL)
- Support ReqRes auth association + JSONPlaceholder business association
- CI/local compatibility (mock token fallback)
"""
import requests
from config.config import (
    REQRES_BASE_URL,
    JSONPLACEHOLDER_BASE_URL,
    REQUEST_TIMEOUT,
    SSL_VERIFY,
    COMMON_HEADERS,
    REQRES_MOCK_TOKEN,
    REQRES_TEST_USER
)
# Import logger (replace print)
from config.log_config import logger

# Disable SSL warnings for test environment
requests.packages.urllib3.disable_warnings()

class HttpRequest:
    def __init__(self):
        """Initialize request object with empty base URL (switch via scenario methods)"""
        self.base_url = ""
        self.headers = COMMON_HEADERS.copy()
        self.token = None  # Store ReqRes auth token

    def reqres_login(self) -> str:
        """
        ReqRes login wrapper: get auth token (real/mock)
        Auto use test account from config, fallback to mock token for CI
        :return: Auth token (real/mock)
        """
        self.base_url = REQRES_BASE_URL
        login_url = "/api/login"
        login_payload = {
            "email": REQRES_TEST_USER["email"],
            "password": REQRES_TEST_USER["password"]
        }

        try:
            resp = self.post(login_url, json=login_payload)
            if resp.status_code == 200:
                self.token = resp.json()["token"]
                logger.info(f"ReqRes login success | Token: {self.token[:8]}...")  # Replace print
                return self.token
            else:
                logger.warning(f"ReqRes login failed (status code {resp.status_code}), use mock token")  # Replace print
                self.token = REQRES_MOCK_TOKEN
                return self.token
        except Exception:
            logger.warning("ReqRes login request exception, use mock token")  # Replace print
            self.token = REQRES_MOCK_TOKEN
            return self.token

    # ... 其余GET/POST/switch方法不变 ...

# Global request instance (import and use directly in test cases)
http = HttpRequest()
