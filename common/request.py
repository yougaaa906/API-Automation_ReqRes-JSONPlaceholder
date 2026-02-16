# -*- coding: utf-8 -*-
"""
HTTP请求封装类：
适配场景：ReqRes鉴权关联 + JSONPlaceholder业务关联
完全兼容config.py配置，无未定义变量，CI/本地双环境稳定
"""
import requests
# 导入config配置（仅保留当前实际用到的变量）
from config.config import (
    REQRES_BASE_URL,
    JSONPLACEHOLDER_BASE_URL,
    REQUEST_TIMEOUT,
    SSL_VERIFY,
    COMMON_HEADERS,
    REQRES_MOCK_TOKEN,
    REQRES_TEST_USER
)

# 禁用SSL警告（适配所有测试接口）
requests.packages.urllib3.disable_warnings()

class HttpRequest:
    def __init__(self):
        """初始化：清空旧的冗余逻辑，适配双场景Base URL"""
        # 初始Base URL为空，通过switch方法切换场景
        self.base_url = ""
        # 全局请求头：直接复用config中的COMMON_HEADERS，避免重复定义
        self.headers = COMMON_HEADERS.copy()
        # 存储ReqRes鉴权Token
        self.token = None

    # -------------------------- ReqRes专属：登录获取Token（鉴权关联核心） --------------------------
    def reqres_login(self) -> str:
        """
        ReqRes登录封装：自动使用config中的测试账号，适配本地/CI环境
        返回：真实Token（本地）/Mock Token（CI）
        """
        # 切换到ReqRes的Base URL
        self.base_url = REQRES_BASE_URL
        login_url = "/api/login"
        # 使用config中统一管理的测试账号
        login_payload = {
            "email": REQRES_TEST_USER["email"],
            "password": REQRES_TEST_USER["password"]
        }

        try:
            resp = self.post(login_url, json=login_payload)
            if resp.status_code == 200:
                self.token = resp.json()["token"]
                print(f"✅ ReqRes登录成功 | Token: {self.token[:8]}...")
                return self.token
            else:
                # CI风控/登录失败时返回Mock Token
                print(f"⚠️ ReqRes登录失败（状态码{resp.status_code}），使用Mock Token")
                self.token = REQRES_MOCK_TOKEN
                return self.token
        except Exception:
            # 异常时返回Mock Token，保证CI不崩溃
            print("⚠️ ReqRes登录请求异常，使用Mock Token")
            self.token = REQRES_MOCK_TOKEN
            return self.token

    # -------------------------- 通用GET请求封装 --------------------------
    def get(self, url: str, headers: dict = None) -> requests.Response:
        """
        通用GET请求：支持完整URL/相对路径，自动拼接Base URL
        :param url: 接口地址（完整URL或相对路径）
        :param headers: 自定义请求头（可选）
        :return: requests.Response
        """
        # 拼接完整URL（如果是相对路径）
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        # 合并请求头（全局头 + 自定义头）
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        try:
            return requests.get(
                url=full_url,
                headers=final_headers,
                timeout=REQUEST_TIMEOUT,
                verify=SSL_VERIFY
            )
        except Exception as e:
            raise Exception(f"GET请求失败 | URL: {full_url} | 错误: {str(e)}")

    # -------------------------- 通用POST请求封装 --------------------------
    def post(self, url: str, json: dict = None, headers: dict = None) -> requests.Response:
        """
        通用POST请求：支持完整URL/相对路径，自动拼接Base URL
        :param url: 接口地址（完整URL或相对路径）
        :param headers: 自定义请求头（可选）
        :param json: POST请求体（JSON格式）
        :return: requests.Response
        """
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        try:
            return requests.post(
                url=full_url,
                json=json,
                headers=final_headers,
                timeout=REQUEST_TIMEOUT,
                verify=SSL_VERIFY
            )
        except Exception as e:
            raise Exception(f"POST请求失败 | URL: {full_url} | 错误: {str(e)}")

    # -------------------------- 快捷切换场景Base URL --------------------------
    def switch_to_reqres(self):
        """切换到ReqRes场景的Base URL"""
        self.base_url = REQRES_BASE_URL

    def switch_to_jsonplaceholder(self):
        """切换到JSONPlaceholder场景的Base URL"""
        self.base_url = JSONPLACEHOLDER_BASE_URL

# 全局实例化，测试用例直接导入使用
http = HttpRequest()
