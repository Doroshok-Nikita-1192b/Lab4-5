from pydantic import BaseModel
from datetime import date

class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_adress: str
    contract_number: int
    data_contract: date
    count_delivery: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    shipment_id: int
    product_id: int

    class Config:
        orm_mode = True




class ProductBase(BaseModel):
    product_name: str
    product_price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    order: list[Order]

    class Config:
        orm_mode = True



class ShipmentBase(BaseModel):
    shipment_date: date #библиотека Type, Docs sqlalchemy
    shipment_count: int

class ShipmentCreate(ShipmentBase):

    pass

class Shipment(ShipmentBase):
    id: int
    order: list[Order]

    class Config:
        orm_mode = True