# -*- coding: utf-8 -*-
"""
Saucedemo API自动化用例：聚焦接口关联、正向/负向场景
"""
from common.request import http
import pytest

# 固件：登录获取有效token（接口关联前置）
@pytest.fixture(scope="module")
def saucedemo_login_token():
    """登录saucedemo，返回有效token"""
    # saucedemo官方测试账号（无风控，100%可用）
    response = http.login(username="standard_user", password="secret_sauce")
    # 断言登录成功
    assert response.status_code == 200, f"登录失败 - 状态码: {response.status_code}"
    assert http.session_token is not None, "登录后未获取到token"
    yield http.session_token

# 用例1：登录后获取商品列表（正向场景+接口关联）
def test_get_products_with_valid_token(saucedemo_login_token):
    api_url = f"{http.base_url}/inventory-api/item"
    response = http.get(url=api_url)
    res_data = response.json()

    # 核心断言
    assert response.status_code == 200, f"预期状态码200，实际: {response.status_code}"
    assert isinstance(res_data, list), "商品列表应为数组类型"
    assert len(res_data) > 0, "商品列表不能为空"
    assert "id" in res_data[0], "商品数据缺少id字段"
    print("✅ 用例1通过：登录后获取商品列表成功")

# 用例2：错误密码登录（负向场景）
def test_login_with_wrong_password():
    response = http.login(username="standard_user", password="wrong_password_123")
    # saucedemo错误密码返回401
    assert response.status_code == 401, f"预期状态码401，实际: {response.status_code}"
    print("✅ 用例2通过：错误密码登录失败（符合预期）")

# 用例3：空密码登录（边界场景）
def test_login_with_empty_password():
    response = http.login(username="standard_user", password="")
    assert response.status_code == 401, f"预期状态码401，实际: {response.status_code}"
    print("✅ 用例3通过：空密码登录失败（符合预期）")
