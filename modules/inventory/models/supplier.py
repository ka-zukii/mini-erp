from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

# Model Supplier
class Supplier(Base):
    # Nama tabel dalam database
    __tablename__ = "supplier"
    
    # Mendefinisikan kolom-kolom pada tabel supplier
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama = Column(String, nullable=False)
    telepon = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    id_gudang = Column(String, ForeignKey("gudang.id", ondelete="CASCADE"), nullable=False)
    
    # Relasi dengan model Gudang sebagai child
    gudang = relationship("Gudang", back_populates="supplier_list")
    
    # Relasi dengan model Barang sebagai parent
    barang_list = relationship("Barang", back_populates='supplier', cascade="all, delete")