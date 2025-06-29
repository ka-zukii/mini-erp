from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

class Gudang(Base):
    __tablename__ = "gudang"

    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama = Column(String, nullable=False)
    lokasi = Column(String, nullable=True)
    keterangan = Column(String, nullable=True)
    
    log_gudang = relationship("LogAktivitas", back_populates="gudang", cascade="all, delete")
    pengguna_list = relationship("Pengguna", back_populates="gudang", cascade="all, delete")
    barang_list = relationship("Barang", back_populates="gudang", cascade="all, delete")
    kategori_list = relationship("Kategori", back_populates="gudang", cascade="all, delete")
    transaksi_list = relationship("Transaksi", back_populates="gudang", cascade="all, delete")