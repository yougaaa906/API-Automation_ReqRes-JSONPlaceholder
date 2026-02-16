# -*- coding: utf-8 -*-
"""
配置文件：统一管理环境变量、接口地址、通用配置（贴近真实工作规范）
"""
import os

# -------------------------- 环境配置 --------------------------
# 环境选择：优先从CI环境变量读取，本地默认test
ENV = os.getenv("TEST_ENV", "test")

# -------------------------- 接口基础配置 --------------------------
# 多环境base_url（saucedemo只有test环境，仅做示例）
BASE_URLS = {
    "test": "https://www.saucedemo.com",
    "prod": "https://www.saucedemo.com"  # 示例：实际工作中会区分
}
# 最终使用的base_url
API_BASE_URL = BASE_URLS[ENV]

# -------------------------- 请求配置 --------------------------
# 请求超时时间（秒）
REQUEST_TIMEOUT = 10
# SSL验证（固定False，适配saucedemo）
SSL_VERIFY = False

# -------------------------- 测试账号配置 --------------------------
# saucedemo官方测试账号（CI中可从Secrets读取，本地用默认值）
TEST_USERNAME = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
TEST_PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
