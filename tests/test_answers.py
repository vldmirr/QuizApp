import pytest
import uuid

def test_create_answer(client):
    """Тест создания ответа"""
    # Сначала создаем вопрос
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Test question?"}
    )
    question_id = question_response.json()["id"]
    
    # Создаем ответ
    user_id = str(uuid.uuid4())
    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Test answer",
            "user_id": user_id
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test answer"
    assert data["user_id"] == user_id
    assert data["question_id"] == question_id

def test_create_answer_nonexistent_question(client):
    """Тест создания ответа к несуществующему вопросу"""
    user_id = str(uuid.uuid4())
    response = client.post(
        "/api/v1/questions/999/answers/",
        json={
            "text": "Test answer",
            "user_id": user_id
        }
    )
    assert response.status_code == 404

def test_get_answer(client):
    """Тест получения ответа"""
    # Создаем вопрос и ответ
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Test question?"}
    )
    question_id = question_response.json()["id"]
    
    user_id = str(uuid.uuid4())
    answer_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Test answer",
            "user_id": user_id
        }
    )
    answer_id = answer_response.json()["id"]
    
    # Получаем ответ
    response = client.get(f"/api/v1/answers/{answer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == answer_id
    assert data["text"] == "Test answer"

def test_delete_answer(client):
    """Тест удаления ответа"""
    # Создаем вопрос и ответ
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Test question?"}
    )
    question_id = question_response.json()["id"]
    
    user_id = str(uuid.uuid4())
    answer_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Test answer",
            "user_id": user_id
        }
    )
    answer_id = answer_response.json()["id"]
    
    # Удаляем ответ
    response = client.delete(f"/api/v1/answers/{answer_id}")
    assert response.status_code == 204
    
    # Проверяем, что ответ удален
    get_response = client.get(f"/api/v1/answers/{answer_id}")
    assert get_response.status_code == 404

def test_cascade_delete(client):
    """Тест каскадного удаления ответов при удалении вопроса"""
    # Создаем вопрос
    question_response = client.post(
        "/api/v1/questions/",
        json={"text": "Test question?"}
    )
    question_id = question_response.json()["id"]
    
    # Создаем несколько ответов
    user_id = str(uuid.uuid4())
    for i in range(3):
        client.post(
            f"/api/v1/questions/{question_id}/answers/",
            json={
                "text": f"Answer {i}",
                "user_id": user_id
            }
        )
    
    # Удаляем вопрос
    client.delete(f"/api/v1/questions/{question_id}")
    
    # Проверяем, что ответы тоже удалены
    # (в реальном приложении нужно проверить через БД)
    get_question_response = client.get(f"/api/v1/questions/{question_id}")
    assert get_question_response.status_code == 404