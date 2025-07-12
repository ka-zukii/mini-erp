from sqlalchemy.orm import Session
from modules.inventory.models.barang import Barang
from modules.inventory.schemas.barang_schema import BarangCreate, BarangUpdate

class BarangService:
    def get_all(db: Session):
        return db.query(Barang).all()
    
    def get_by_id(db: Session, id: str):
        return db.query(Barang).filter(Barang.id == id).first()
    
    def store(db: Session, data: BarangCreate):
        data_barang = Barang(
            kd_barang = data.kd_barang,
            nama = data.nama,
            deskripsi = data.deskripsi,
            satuan = data.satuan,
            harga_beli = data.harga_beli,
            harga_jual = data.harga_jual,
            stock = data.stock,
            id_kategori = data.id_kategori,
            id_supplier = data.id_supplier,
            id_gudang = data.id_gudang
        )
        
        db.add(data_barang)
        db.commit()
        db.refresh(data_barang)
        return data_barang
    
    def update(db: Session, id: str, data: BarangUpdate):
        barang = db.query(Barang).filter(Barang.id == id).first()
        
        if not barang:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(barang, field, value)
        
        db.commit()
        db.refresh(barang)
        return barang
    
    def destroy(db: Session, id: str):
        barang = db.query(Barang).filter(Barang.id == id).first()
        
        if not barang:
            return False
        
        db.delete(barang)
        db.commit()
        return True