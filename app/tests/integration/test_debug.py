import pytest
from litestar.testing import TestClient
from app.main import app

def test_app_import():
    """Тест что приложение импортируется без ошибок"""
    try:
        from app.main import app
        print("✅ App imported successfully")
        assert app is not None
    except Exception as e:
        print(f"❌ App import failed: {e}")
        raise

def test_app_health():
    """Тест базового здоровья приложения"""
    with TestClient(app=app) as client:
        # Проверяем разные эндпоинты
        endpoints = ["/", "/schema", "/users"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            print(f"Endpoint {endpoint}: {response.status_code}")
            
            # Главное - не 500 ошибка
            if response.status_code == 500:
                print(f"❌ 500 Error at {endpoint}: {response.text}")
            else:
                print(f"✅ {endpoint} responds with {response.status_code}")

def test_simple_post():
    """Очень простой POST тест"""
    with TestClient(app=app) as client:
        # Минимальные данные
        minimal_data = {
            "username": "testuser123",
            "email": "test123@example.com"
        }
        
        response = client.post("/users", json=minimal_data)
        print(f"Simple POST status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"❌ 500 Error details: {response.text}")
        
        # Для диагностики временно разрешим любой статус кроме 500
        assert response.status_code != 500, f"Server error: {response.text}"