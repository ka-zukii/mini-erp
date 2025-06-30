from sqlalchemy.orm import Session
from modules.inventory.schemas.gudang_schema import GudangCreate, GudangUpdate
from modules.inventory.models import *

class GudangService:
    def get_all(db: Session):
        return db.query(Gudang).all()
    
    def get_by_id(db: Session, id: str):
        return db.query(Gudang).filter(Gudang.id == id).first()
    
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
    
    def update(db: Session, id: str, data: GudangUpdate):
        gudang = db.query(Gudang).filter(Gudang.id == id).first()
        
        if not gudang:
            return None
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(gudang, field, value)
        
        db.commit()
        db.refresh()
        return gudang
    
    def destroy(db: Session, id: str):
        gudang = db.query(Gudang).filter(Gudang.id == id).first()
        
        if not gudang:
            return False
        
        db.delete(Gudang)
        db.commit()
        return True