from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    """
    Задаем зависимость к БД. При каждом запросе будет создаваться новое
    подключение.
    """
    db = SessionLocal() # pragma: no cover
    try: # pragma: no cover
        yield db # pragma: no cover
    finally: # pragma: no cover
        db.close() # pragma: no cover

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):

    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    db_product = crud.get_product_by_name(db, product_name=product.product_name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product name is already exist")
    return crud.create_product(db=db, product=product)



@app.post("/shipments/", response_model=schemas.Shipment)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    
    return crud.create_shipment(db=db, shipment=shipment)


@app.get("/shipments/", response_model=list[schemas.Shipment])
def read_shipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    shipments = crud.get_shipments(db, skip=skip, limit=limit)
    return shipments

@app.get("/shipments/{shipment_id}", response_model=schemas.Shipment)
def read_product_by_id(shipment_id: int, db: Session = Depends(get_db)):

    db_shipment = crud.get_shipment_by_id(db, shipment_id=shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment


@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order_by_id(order_id: int, db: Session = Depends(get_db)):

    db_order = crud.get_order_by_id(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.post("/orders/{shipment_id}/{product_id}/", response_model=schemas.Order)
def create_order(
    shipment_id: int, product_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)
):  
    return crud.create_order(db=db, order=order, product_id=product_id, shipment_id=shipment_id)