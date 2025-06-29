from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

class Kategori(Base):
    __tablename__ = "kategori"
    
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama = Column(String, nullable=False)
    deskripsi = Column(String, nullable=False)

    id_gudang = Column(String, ForeignKey('gudang.id', ondelete='CASCADE'), nullable=False)

    gudang = relationship('Gudang', back_populates='kategori_list')
    
    barang_list = relationship("Barang", back_populates="kategori", cascade="all, delete")