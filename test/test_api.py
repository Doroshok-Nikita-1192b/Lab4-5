from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./Tsqlite_base.db"  # Тестовая БД

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению

def test_create_product():
    response = client.post(
        "/products/",
        json={"product_name": "Кругетс", "product_price": "100"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "Кругетс"

def test_create_exist_product():
    response = client.post(
        "/products/",
        json={"product_name": "Кругетс", "product_price": "100"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Product name is already exist"

def test_read_product():
    response = client.get("/products/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["product_name"] == "Кругетс"

def test_get_product_by_id():
    response = client.get("/products/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "Кругетс"

def test_product_not_found():
    response = client.get("/products/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Product not found"

def test_create_shipment():
    response = client.post(
        "/shipments/",
        json={"shipment_date": "2079-12-12", "shipment_count": "10"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["shipment_date"] == "2079-12-12"

def test_read_shipment():
    response = client.get("/shipments/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["shipment_date"] == "2079-12-12"

def test_get_shipment_by_id():
    response = client.get("/shipments/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["shipment_date"] == "2079-12-12"

def test_shipment_not_found():
    response = client.get("/shipments/4")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Shipment not found"

    
def test_create_order():
    response = client.post(
        "/orders/1/1/",
        json={
            "customer_name": "ДораДура", 
            "customer_phone": "+777",
            "customer_adress": "Ул. Пушкина дом Колотушкина",
            "contract_number": 333,
            "data_contract": '2023-12-05',
            "count_delivery": 3,
            "product_id": 1,
            "shipment_id":1

    }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["customer_name"] == "ДораДура"
    assert data["customer_phone"] == "+777"
    assert data["customer_adress"] == "Ул. Пушкина дом Колотушкина"
    assert data["contract_number"] == 333
    assert data["data_contract"] == '2023-12-05'
    assert data["count_delivery"] == 3
    assert data["product_id"] == 1
    assert data["shipment_id"] == 1

def test_get_order_by_id():
    response = client.get("/orders/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["customer_name"] == "ДораДура"

def test_read_order():
    response = client.get("/orders/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["customer_name"] == "ДораДура"

def test_order_not_found():
    response = client.get("/orders/4")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Order not found"