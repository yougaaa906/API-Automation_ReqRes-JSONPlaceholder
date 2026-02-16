# -*- coding: utf-8 -*-
"""
JSONPlaceholder business parameter association test cases
Core: Create resource → Extract ID → Query associated resource
Feature: 100% rate-limit free, stable for CI execution
"""
from common.request import http
from config.log_config import logger  # Import logger

def test_create_post_then_get_comments():
    """Positive case: Create post → Extract postId → Query comments (business association)"""
    http.switch_to_jsonplaceholder()
    
    # Step 1: Create post and extract business parameter (postId)
    create_payload = {
        "title": "CI_TEST_business_association",
        "body": "API automation - business parameter association test",
        "userId": 1
    }
    create_resp = http.post("/posts", json=create_payload)
    assert create_resp.status_code == 201, f"Post creation failed, status code {create_resp.status_code}"
    post_id = create_resp.json()["id"]
    assert post_id is not None, "Post creation returned empty postId"
    logger.info(f"Post created successfully, extracted postId: {post_id}")  # Replace print
    
    # Step 2: Query comments with postId (business parameter transfer)
    get_resp = http.get(f"/comments?postId={post_id}")
    assert get_resp.status_code == 200, f"Comment query failed, status code {get_resp.status_code}"
    # JSONPlaceholder is mock API, new postId has no real comments
    assert len(get_resp.json()) == 0, "JSONPlaceholder mock API: no real comments for new postId"
    logger.info("Business association test passed: postId transferred successfully (mock API behavior)")  # Replace print

def test_get_post_then_get_user():
    """Extended case: Get post → Extract userId → Query associated user (multi-layer association)"""
    http.switch_to_jsonplaceholder()
    
    # Step 1: Get post and extract userId
    post_resp = http.get("/posts/1")
    assert post_resp.status_code == 200, "Post query failed"
    user_id = post_resp.json()["userId"]
    assert user_id == 1, "Post userId mismatch"
    
    # Step 2: Query user with userId
    user_resp = http.get(f"/users/{user_id}")
    assert user_resp.status_code == 200, "User query failed"
    assert user_resp.json()["id"] == user_id, "User ID mismatch"
    logger.info("Multi-layer business association test passed: userId transferred successfully")  # Replace print
