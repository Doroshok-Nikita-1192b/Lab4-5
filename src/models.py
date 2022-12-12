from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):
    """
    Абстартный базовый класс, где описаны все поля и методы по умолчанию
    """
    __abstract__ = True

    id = Column(Integer, primary_key = True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>" # pragma: no cover

class Product(BaseModel):
    __tablename__ = "products"

    product_name = Column(String)
    product_price = Column(Float)

    order = relationship("Order", back_populates="product")

class Order(BaseModel):
    __tablename__ = "orders"

    customer_name = Column(String)
    customer_phone = Column(String)
    customer_adress = Column(String)
    contract_number = Column(Integer)
    data_contract = Column(DateTime)
    count_delivery = Column(Integer)

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="order")

    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    shipment = relationship("Shipment", back_populates="order")


class Shipment(BaseModel):
    __tablename__ = "shipments"

    shipment_date = Column(DateTime) #просмотреть формат даты
    shipment_count = Column(Integer)

    order = relationship("Order", back_populates="shipment")
