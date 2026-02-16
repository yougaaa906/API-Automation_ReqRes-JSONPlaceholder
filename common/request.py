# -*- coding: utf-8 -*-
"""
HTTP请求封装：适配saucedemo API，通用可复用
"""
import requests

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings()

class HttpRequest:
    def __init__(self, base_url: str):
        self.base_url = base_url
        # 通用请求头（saucedemo 无需复杂头，基础即可）
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.session_token = None  # 存储登录后的会话标识

    def login(self, username: str, password: str) -> requests.Response:
        """封装saucedemo登录接口（接口关联核心）"""
        login_url = f"{self.base_url}/api/login"
        payload = {
            "userName": username,
            "password": password
        }
        response = self.post(url=login_url, json=payload)
        # 保存登录token（saucedemo登录成功返回的token字段）
        if response.status_code == 200:
            self.session_token = response.json().get("token")
            self.headers["Authorization"] = f"Bearer {self.session_token}"
        return response

    def get(self, url: str, headers: dict = None) -> requests.Response:
        """通用GET请求封装"""
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)
        try:
            return requests.get(
                url=url,
                headers=final_headers,
                timeout=10,
                verify=False
            )
        except Exception as e:
            raise Exception(f"GET请求失败 - URL: {url}, 错误: {str(e)}")

    def post(self, url: str, json: dict = None, headers: dict = None) -> requests.Response:
        """通用POST请求封装"""
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)
        try:
            return requests.post(
                url=url,
                headers=final_headers,
                json=json,
                timeout=10,
                verify=False
            )
        except Exception as e:
            raise Exception(f"POST请求失败 - URL: {url}, 错误: {str(e)}")

# 初始化saucedemo请求对象（固定base_url，无需配置文件）
http = HttpRequest(base_url="https://www.saucedemo.com")
