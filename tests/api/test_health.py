def test_root_answers_below_500(client):
    response = client.get("")
    assert response.status_code < 500
