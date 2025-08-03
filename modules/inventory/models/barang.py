from sqlalchemy import Column, Integer, String, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

# Model Barang
class Barang(Base):
    # Nama tabel dalam database
    __tablename__ = "barang"
    
    # Mendefinisikan kolom-kolom pada tabel barang
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    kd_barang = Column(String, nullable=False, index=True, unique=True)
    nama = Column(String, nullable=False)
    deskripsi = Column(String, nullable=True)
    satuan = Column(Enum('pcs', 'kg', 'liter', name='satuan_enum'), nullable=False)
    harga_beli = Column(DECIMAL, nullable=False)
    harga_jual = Column(DECIMAL, nullable=True)
    stock = Column(Integer, nullable=False)
    
    # Foreign key untuk kategori, supplier, dan gudang
    id_kategori = Column(String, ForeignKey('kategori.id', ondelete='CASCADE'), nullable=True)
    id_supplier = Column(String, ForeignKey('supplier.id', ondelete='CASCADE'), nullable=True)
    id_gudang = Column(String, ForeignKey('gudang.id', ondelete='CASCADE'), nullable=False)
    
    # Relasi dengan model lain sebagai child
    gudang = relationship('Gudang', back_populates='barang_list')
    kategori = relationship("Kategori", back_populates="barang_list")
    supplier = relationship('Supplier', back_populates='barang_list')
    
    # Relasi dengan model Transaksi sebagai parent
    transaksi_list = relationship("Transaksi", back_populates="barang", cascade="all, delete")