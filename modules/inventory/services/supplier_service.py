from sqlalchemy.orm import Session
from modules.inventory.schemas.supplier_schema import SupplierCreate, SupplierUpdate
from modules.inventory.models import *

class SupplierService:
    def get_all(db: Session):
        return db.query(Supplier).all()
    
    def get_by_id(db: Session, id: str):
        return db.query(Supplier).filter(Supplier.id == id).first()
    
    def store(db: Session, data: SupplierCreate):
        data_supplier = Supplier(
            nama = data.nama,
            telepon = data.telepon,
            alamat = data.alamat
        )
        
        db.add(data_supplier)
        db.commit()
        db.refresh(data_supplier)
        return data_supplier
    
    def update(db: Session, id: str, data: SupplierUpdate):
        supplier = db.query(Supplier).filter(Supplier.id == id).first()
        
        if not supplier:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(supplier, field, value)
        
        db.commit()
        db.refresh(supplier)
        return supplier
    
    def destroy(db: Session, id: str):
        supplier = db.query(Supplier).filter(Supplier.id == id).first()
        
        if not supplier:
            return False
        
        db.delete(supplier)
        db.commit()
        return True