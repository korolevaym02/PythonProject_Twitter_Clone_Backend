import pytest
from fastapi.testclient import TestClient


def test_create_tweet(client: TestClient, create_test_users):
    """Тест создания твита."""
    users = create_test_users
    response = client.post(
        "/api/tweets",
        headers={"api-key": users["user1"]["api_key"]},
        data={"tweet_data": "Test tweet"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweet_id" in data
    assert data["tweet_id"] > 0


def test_get_feed(client: TestClient, create_test_users):
    """Тест получения ленты."""
    users = create_test_users
    response = client.get(
        "/api/tweets",
        headers={"api-key": users["user1"]["api_key"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True