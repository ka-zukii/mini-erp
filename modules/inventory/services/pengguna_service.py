from sqlalchemy.orm import Session
from modules.inventory.schemas.pengguna_schema import PenggunaCreate, PenggunaUpdate
from modules.inventory.models import *

class PenggunaService:
    def get_all(db: Session):
        return db.query(Pengguna).all()
    
    def get_by_id(db: Session, id: str):
        return db.query(Pengguna).filter(Pengguna.id == id).first()
    
    def store(db: Session, data:PenggunaCreate):
        data_pengguna = Pengguna(
            nama_lengkap= data.nama_lengkap,
            username= data.username,
            password= data.password,
            role= data.role,
            refresh_token= data.refresh_token,
            sign_status= data.sign_status,
            id_gudang = data.id_gudang
        )
        
        db.add(data_pengguna)
        db.commit()
        db.refresh(data_pengguna)
        return data_pengguna
    
    def update(db: Session, id: str, data:PenggunaUpdate):
        pengguna = db.query(Pengguna).filter(Pengguna.id == id).first()
        
        if not pengguna:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(pengguna, field, value)
        
        db.commit()
        db.refresh(pengguna)
        return pengguna
    
    def destroy(db: Session, id:str):
        pengguna = db.query(Pengguna).filter(Pengguna.id == id).first()
        
        if not pengguna:
            return False
        
        db.delete(pengguna)
        db.commit()
        return True