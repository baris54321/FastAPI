from fastapi import APIRouter, Depends, HTTPException
from utils.helpers import has_exception
from sqlalchemy.orm import Session
from db.session import get_db_session
from crud.product_crud import *
from services.token_services import create_access_token, create_refresh_token, get_current_user 
from schemas.product import ProductCreate, ProductResponse, ProductOut, DeleteProduct, ProductUpdate
from models.user import User
from datetime import datetime


router = APIRouter()

# Create a new product
@router.post("/add_products", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin")
        
        if db.query(Product).filter(Product.name == product.name).filter(Product.deleted_at.is_(None)).first():
            raise HTTPException(status_code=400, detail="Product with this name already exists")

        product_data = create_product(db, product, current_user.id)

        return {
            "data": product_data,
            "message": "Product added successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all products
@router.get("/all_products", response_model=list[ProductOut])
def get_all_products(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin")
        
        products = []        
        if current_user.is_admin:
            products = db.query(Product).filter(Product.deleted_at.is_(None)).all()
        else:
            products = db.query(Product).filter(Product.owner_id == current_user.id).filter(Product.deleted_at.is_(None)).all()
      
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# update the product
@router.put("/update_product/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin")
        
        db_product = db.query(Product).filter(Product.id == product_id).filter(Product.deleted_at.is_(None)).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if not current_user.is_admin and db_product.owner_id != current_user.id :
            raise HTTPException(status_code=403, detail="You do not have permission to update this product")
        
        # check prduct name exist 
        existing_product = db.query(Product).filter(
                Product.name == product.name,
                Product.id != product_id  
            ).filter(Product.deleted_at.is_(None)).first()

        if existing_product:
            raise HTTPException(status_code=400, detail="Product with this name already exists")
        
        db_product.name = product.name if product.name else db_product.name
        db_product.description = product.description if product.description else db_product.description
        db_product.price = product.price if product.price else db_product.price
        db_product.updated_by = current_user.id 
        db_product.updated_at = datetime.utcnow()
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        return {
            "data": db_product,
            "message": "Product updated successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Delete a product
@router.delete("/delete_product/{product_id}", response_model= DeleteProduct)
def delete_product(product_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin")
        
        db_product = db.query(Product).filter(Product.id == product_id).filter(Product.deleted_at.is_(None)).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if not current_user.is_admin and db_product.owner_id != current_user.id :
            raise HTTPException(status_code=403, detail="You do not have permission to delete this product")
        
        db_product.deleted_by = current_user.id
        db_product.deleted_at = datetime.utcnow()
        db.add(db_product)
        db.commit()
        
        return {
            "message": "Product deleted successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#  Get PArticulre product by ID
@router.get("/get_product/{product_id}", response_model= ProductCreate)
def get_product(product_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin")
       
        db_product = db.query(Product).filter(Product.id == product_id).filter(Product.deleted_at.is_(None)).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if not current_user.is_admin and db_product.owner_id != current_user.id :
            raise HTTPException(status_code=403, detail="You do not have permission to view this product")
        
        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
                