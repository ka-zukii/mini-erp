from sqlalchemy.orm import Session
from sqlalchemy import func
from modules.inventory.models.barang import Barang
from modules.inventory.schemas.barang_schema import BarangCreate, BarangUpdate

# Service untuk mengelola operasi bisnis pada model Barang
class BarangService:
    # Metode statis untuk mengambil seluruh data barang
    @staticmethod
    def get_all(db: Session):
        return db.query(Barang).all()
    
    # Metode statis untuk mengambil data barang berdasarkan ID
    @staticmethod
    def get_by_id(db: Session, id: str):
        return db.query(Barang).filter(Barang.id == id).first()
    
    # Metode statis untuk menyimpan data barang baru
    @staticmethod
    def store(db: Session, data: BarangCreate):
        data_barang = Barang(
            kd_barang = BarangService.generate_kode_barang(db),
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
    
    # Metode statis untuk memperbarui data barang berdasarkan ID
    @staticmethod
    def update(db: Session, id: str, data: BarangUpdate):
        barang = db.query(Barang).filter(Barang.id == id).first()
        
        if not barang:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(barang, field, value)
        
        db.commit()
        db.refresh(barang)
        return barang
    
    # Metode statis untuk menghapus data barang berdasarkan ID
    @staticmethod
    def destroy(db: Session, id: str):
        barang = db.query(Barang).filter(Barang.id == id).first()
        
        if not barang:
            return False
        
        db.delete(barang)
        db.commit()
        return True
    def generate_kode_barang(db: Session):
        # Mengambil kode barang terakhir
        last = db.query(Barang).order_by(Barang.kd_barang.desc()).first()
        if last:
            last_number = int(last.kd_barang.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        return f"BRG-{new_number:03d}"