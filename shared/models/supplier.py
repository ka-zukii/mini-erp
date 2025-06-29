from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from shared.database.db import Base, generate_cuid

class Supplier(Base):
    __tablename__ = "supplier"
    
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama = Column(String, nullable=False)
    telepon = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    id_barang = Column(String, ForeignKey("barang.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    barang = relationship("Barang", back_populates="supplier_list")