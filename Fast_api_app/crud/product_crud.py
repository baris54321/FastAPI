from sqlalchemy.orm import Session
from models.products import Product
from schemas.product import ProductCreate


def create_product(db: Session, product: ProductCreate, owner_id: int) -> Product:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        owner_id=owner_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product