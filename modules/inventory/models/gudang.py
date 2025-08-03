from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

# Model Gudang
class Gudang(Base):
    # Nama tabel dalam database
    __tablename__ = "gudang"

    # Mendefinisikan kolom-kolom pada tabel gudang
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama = Column(String, nullable=False)
    lokasi = Column(String, nullable=True)
    keterangan = Column(String, nullable=True)

    # Relasi dengan model lain sebagai parent
    barang_list = relationship("Barang", back_populates="gudang", cascade="all, delete")
    kategori_list = relationship("Kategori", back_populates="gudang", cascade="all, delete")
    transaksi_list = relationship("Transaksi", back_populates="gudang", cascade="all, delete")
