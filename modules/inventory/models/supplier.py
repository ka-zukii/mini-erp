from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

class Supplier(Base):
    __tablename__ = "supplier"
    
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama = Column(String, nullable=False)
    telepon = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    
    barang_list = relationship("Barang", back_populates='supplier', cascade="all, delete")