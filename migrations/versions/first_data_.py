"""empty message

Revision ID: first_data
Revises: a0e71fdffd1a
Create Date: 2022-12-12 00:00:51.164956

"""
from alembic import op
from sqlalchemy import orm

from src.models import Order, Product, Shipment
from datetime import datetime
# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = 'a0e71fdffd1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    cool_product = Product(product_name='Унитаз', product_price=7000)
    bad_product = Product(product_name='Плитка', product_price=150)

    session.add_all([cool_product, bad_product])
    session.flush()


    shipment1 = Shipment(shipment_date=datetime(2022, 12, 12), shipment_count=10)
    shipment2 = Shipment(shipment_date=datetime(2025, 2, 5), shipment_count=2)

    session.add_all([shipment1, shipment2])
    session.flush()

    doroshok = Order(customer_name="Никита Дорошок", customer_phone="+76312", customer_adress="Ул. Пушкина 2", contract_number=2, data_contract=datetime(2030, 1, 4), count_delivery=1, product_id=cool_product.id, shipment_id=shipment1.id)
    nekit = Order(customer_name="Никита Дорошок", customer_phone="+76312", customer_adress="Ул. Пушкина 2", contract_number=2, data_contract=datetime(2030, 1, 4), count_delivery=1, product_id=bad_product.id, shipment_id=shipment2.id)

    session.add_all([doroshok, nekit])
    session.commit()


def downgrade() -> None:
    pass
