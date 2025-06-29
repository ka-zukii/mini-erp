from sqlalchemy import Column, String, Date, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shared.database.db import Base, generate_cuid

class Transaksi(Base):
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    tanggal = Column(Date, nullable=False)
    jenis = Column(Enum('masuk', 'keluar', name="jenis_enum"), nullable=False)
    jumlah = Column(Integer, nullable=False)
    keterangan = Column(String, nullable=True)
    id_barang = Column(String, ForeignKey("barang.id", ondelete="CASCADE"), nullable=False)
    id_gudang = Column(String, ForeignKey("gudang.id", ondelete="CASCADE"), nullable=False)
    
    barang = relationship("Barang", back_populates="transaksi_list")
    gudang = relationship("Gudang", back_populates="transaksi_list")