from sqlalchemy.orm import Session
from modules.inventory.schemas.gudang_schema import GudangCreate, GudangUpdate
from modules.inventory.models import *

# Service untuk mengelola operasi bisnis pada model Gudang

class GudangService:
    # Metode statis untuk mengambil seluruh data gudang
    @staticmethod
    def get_all(db: Session):
        return db.query(Gudang).all()
    
    # Metode statis untuk mengambil data gudang berdasarkan ID
    @staticmethod
    def get_by_id(db: Session, id: str):
        return db.query(Gudang).filter(Gudang.id == id).first()
    
    # Metode statis untuk menyimpan data gudang baru
    @staticmethod
    def store(db: Session, data: GudangCreate):
        data_gudang = Gudang(
            nama = data.nama,
            lokasi = data.lokasi,
            keterangan = data.keterangan
        )
        
        db.add(data_gudang)
        db.commit()
        db.refresh(data_gudang)
        return data_gudang
    
    # Metode statis untuk memperbarui data gudang berdasarkan ID
    @staticmethod
    def update(db: Session, id: str, data: GudangUpdate):
        gudang = db.query(Gudang).filter(Gudang.id == id).first()
        
        if not gudang:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(gudang, field, value)
        
        db.commit()
        db.refresh(gudang)
        return gudang
    
    # Metode statis untuk menghapus data gudang berdasarkan ID
    @staticmethod
    def destroy(db: Session, id: str):
        gudang = db.query(Gudang).filter(Gudang.id == id).first()
        
        if not gudang:
            return False
        
        db.delete(gudang)
        db.commit()
        return True