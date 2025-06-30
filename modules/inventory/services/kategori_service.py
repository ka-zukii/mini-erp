from sqlalchemy.orm import Session
from modules.inventory.schemas.kategori_schema import KategoriCreate, KategoriUpdate
from modules.inventory.models import *

class KategoriService:
    def get_all(db: Session):
        return db.query(Kategori).all()
    
    def get_by_id(db: Session, id: str):
        return db.query(Kategori).filter(Kategori.id == id).first()
    
    def store(db: Session, data: KategoriCreate):
        data_kategori = Kategori(
            nama = data.nama,
            deskripsi = data.deskripsi,
            id_gudang = data.id_gudang
        )
        
        db.add(data_kategori)
        db.commit()
        db.refresh(data_kategori)
        return data_kategori
    
    def update(db: Session, id: str, data: KategoriUpdate):
        kategori = db.query(Kategori).filter(Kategori.id == id).first()
        
        if not kategori:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(kategori, field, value)
        
        db.commit()
        db.refresh(kategori)
        return kategori
    
    def destroy(db: Session, id: str):
        kategori = db.query(Kategori).filter(Kategori.id == id).first()
        
        if not kategori:
            return False
        
        db.delete(kategori)
        db.commit()
        return True