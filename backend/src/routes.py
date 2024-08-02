from datetime import timedelta
from typing import Annotated, List

import controllers as crud
import schemas
import security
from config import settings
from controllers import (create_product, delete_product, get_product,
                         get_products, update_product)
from deps import CurrentUser, SessionDep, get_db
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login/access-token/")
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> schemas.Token:

    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/singup", response_model=schemas.User)
async def create_user(session: SessionDep, user: schemas.UserCreate):
    db_user = crud.get_user(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(session, user)


@router.post("/products/", response_model=schemas.ProductResponse)
def create_product_route(
    product: schemas.ProductCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return create_product(db=db, product=product, current_user=current_user)


@router.get("/products/", response_model=List[schemas.ProductResponse])
def read_all_products_route(db: Session = Depends(get_db)):
    products = get_products(db)
    return products


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/products/{product_id}", response_model=schemas.ProductResponse)
def detele_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product_route(
    product_id: int,
    product: schemas.ProductUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    db_product = update_product(
        db, product_id=product_id, product=product, current_user=current_user
    )
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: CurrentUser, session: SessionDep):
    db_user = crud.get_user(session, user_id=current_user.id)
    return db_user
