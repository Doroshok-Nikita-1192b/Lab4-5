from sqlalchemy.orm import Session

from src import models, schemas

def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(product_name = product.product_name, product_price = product.product_price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_order(db: Session, order: schemas.OrderCreate, product_id: int, shipment_id: int):

    db_order = models.Order(**order.dict(), product_id = product_id, shipment_id = shipment_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def create_shipment(db: Session, shipment: schemas.ShipmentCreate):
    db_shipment = models.Shipment(**shipment.dict())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def get_product_by_id(db: Session, product_id: int):

    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_order_by_id(db: Session, order_id: int):

    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_shipment_by_id(db: Session, shipment_id: int):

    return db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Product).offset(skip).limit(limit).all()

def get_orders(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Order).offset(skip).limit(limit).all()

def get_shipments(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Shipment).offset(skip).limit(limit).all()

def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.product_name == product_name).first()
