from sqlalchemy.orm import Session
from modules.inventory.schemas.transaksi_schema import TransaksiCreate, TransaksiUpdate
from modules.inventory.models import *

class TransaksiService:
    @staticmethod
    def get_all(db: Session):
        return db.query(Transaksi).all()
    
    @staticmethod
    def get_by_id(db: Session, id: str):
        return db.query(Transaksi).filter(Transaksi.id == id).first()
    
    @staticmethod
    def store(db: Session, data: TransaksiCreate):
        data_transaksi = Transaksi(
            tanggal = data.tanggal,
            jenis = data.jenis,
            jumlah = data.jumlah,
            keterangan = data.keterangan,
            id_barang = data.id_barang,
            id_gudang = data.id_gudang
        )
        
        db.add(data_transaksi)
        db.commit()
        db.refresh(data_transaksi)
        return data_transaksi
    
    @staticmethod
    def update(db: Session, id: str, data: TransaksiUpdate):
        transaksi = db.query(Transaksi).filter(Transaksi.id == id).first()
        
        if not transaksi:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(transaksi, field, value)
        
        db.commit()
        db.refresh(transaksi)
        return transaksi
    
    @staticmethod
    def destroy(db: Session, id: str):
        transaksi = db.query(Transaksi).filter(Transaksi.id == id).first()
        
        if not transaksi:
            return False
        
        db.delete(transaksi)
        db.commit()
        return True