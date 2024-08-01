import datetime

from models import ProductModel
from schemas import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session


def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_products(db: Session):
    return db.query(ProductModel).all()


def create_product(db: Session, product: ProductCreate):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None:
        return None

    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.price is not None:
        db_product.price = product.price
    if product.category is not None:
        db_product.category = product.category
    if product.email_provider is not None:
        db_product.email_provider = product.email_provider

    db_product.updated_at = datetime.datetime.now()

    db.commit()
    return db_product
