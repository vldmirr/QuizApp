import pytest

def test_create_question(client):
    """Тест создания вопроса"""
    response = client.post(
        "/api/v1/questions/",
        json={"text": "Test question?"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test question?"
    assert "id" in data
    assert "created_at" in data

def test_get_questions(client):
    """Тест получения списка вопросов"""
    # Сначала создаем вопрос
    client.post("/api/v1/questions/", json={"text": "Test question?"})
    
    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["text"] == "Test question?"

def test_get_question_not_found(client):
    """Тест получения несуществующего вопроса"""
    response = client.get("/api/v1/questions/999")
    assert response.status_code == 404

def test_delete_question(client):
    """Тест удаления вопроса"""
    # Сначала создаем вопрос
    create_response = client.post(
        "/api/v1/questions/",
        json={"text": "Question to delete?"}
    )
    question_id = create_response.json()["id"]
    
    # Удаляем вопрос
    response = client.delete(f"/api/v1/questions/{question_id}")
    assert response.status_code == 204
    
    # Проверяем, что вопрос удален
    get_response = client.get(f"/api/v1/questions/{question_id}")
    assert get_response.status_code == 404

def test_create_question_validation(client):
    """Тест валидации при создании вопроса"""
    response = client.post("/api/v1/questions/", json={"text": ""})
    assert response.status_code == 422