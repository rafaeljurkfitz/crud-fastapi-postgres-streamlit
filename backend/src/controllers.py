import datetime

from models import ProductModel, User
from schemas import ProductCreate, ProductUpdate, UserCreate
from security import get_password_hash, verify_password
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session


def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_products(db: Session):
    return db.query(ProductModel).all()


def create_product(db: Session, product: ProductCreate, current_user: User):
    db_product = ProductModel(
        **product.model_dump(), created_by=current_user.id, updated_by=current_user.id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product


def update_product(
    db: Session, product_id: int, product: ProductUpdate, current_user: User
):
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

    db_product.updated_by = current_user.id
    db_product.updated_at = datetime.datetime.now()

    db.commit()
    return db_product


def get_user(
    db: Session,
    user_id: int | None = None,
    email: str | None = None,
):
    if not any([user_id, email]):
        raise ArgumentError("Must provide user_id or email.")

    query = db.query(User)
    if user_id:
        query = query.filter(User.id == user_id)
    if email:
        query = query.filter(User.email == email)

    return query.first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
#     return (
#         db.query(models.Item)
#         .where(models.Item.owner_id == user_id)
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.model_dump(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


def authenticate(session: Session, email: str, password: str):
    db_user = get_user(db=session, email=email)
    if not db_user or not verify_password(password, db_user.hashed_password):
        return None
    return db_user
