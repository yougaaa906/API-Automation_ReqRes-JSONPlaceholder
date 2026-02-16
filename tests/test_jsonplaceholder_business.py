# -*- coding: utf-8 -*-
"""
JSONPlaceholder 业务参数关联专用用例
核心：创建资源→提取ID→用ID查询关联资源（业务参数关联核心场景）
特点：100%无风控，CI稳定运行
"""
from common.request import http

# -------------------------- 业务参数关联核心用例 --------------------------
def test_create_post_then_get_comments():
    """正向用例：创建文章→提取postId→查询该文章的评论（业务参数关联）"""
    # 切换到JSONPlaceholder场景
    http.switch_to_jsonplaceholder()
    
    # 步骤1：创建文章，提取业务参数（postId）
    create_payload = {
        "title": "CI_TEST_业务关联",
        "body": "接口自动化-业务参数关联测试",
        "userId": 1
    }
    create_resp = http.post("/posts", json=create_payload)
    # 断言创建成功
    assert create_resp.status_code == 201, f"创建文章失败，状态码{create_resp.status_code}"
    post_id = create_resp.json()["id"]  # 提取核心业务参数
    assert post_id is not None, "创建文章未返回postId"
    print(f"✅ 创建文章成功，提取postId：{post_id}")
    
    # 步骤2：用postId查询关联评论（业务参数传递）
    get_resp = http.get(f"/comments?postId={post_id}")
    # 断言关联查询成功
    assert get_resp.status_code == 200, f"查询评论失败，状态码{get_resp.status_code}"
    assert len(get_resp.json()) > 0, "无对应postId的评论（业务关联失败）"
    # 验证所有评论的postId都匹配（精准关联验证）
    for comment in get_resp.json():
        assert comment["postId"] == post_id, f"评论postId不匹配：{comment['postId']} != {post_id}"
    print("✅ 业务参数关联用例通过：postId传递成功，查询到对应评论")

def test_get_post_then_get_user():
    """拓展用例：查询文章→提取userId→查询关联用户（多层业务关联）"""
    http.switch_to_jsonplaceholder()
    
    # 步骤1：查询文章，提取userId
    post_resp = http.get("/posts/1")
    assert post_resp.status_code == 200, "查询文章失败"
    user_id = post_resp.json()["userId"]
    assert user_id == 1, "文章userId不符合预期"
    
    # 步骤2：用userId查询关联用户
    user_resp = http.get(f"/users/{user_id}")
    assert user_resp.status_code == 200, "查询用户失败"
    assert user_resp.json()["id"] == user_id, "用户ID不匹配"
    print("✅ 多层业务关联用例通过：userId传递成功，查询到对应用户")
