from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

# Model Kategori
class Kategori(Base):
    # Nama tabel dalam database
    __tablename__ = "kategori"
    
    # Mendefinisikan kolom-kolom pada tabel kategori
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama = Column(String, nullable=False)
    deskripsi = Column(String, nullable=False)
    
    # Foreign key untuk gudang
    id_gudang = Column(String, ForeignKey('gudang.id', ondelete='CASCADE'), nullable=False)

    # Relasi dengan model lain sebagai child
    gudang = relationship('Gudang', back_populates='kategori_list')
    
    # Relasi dengan model Barang sebagai parent
    barang_list = relationship("Barang", back_populates="kategori", cascade="all, delete")