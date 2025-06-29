from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from shared.database.db import Base, generate_cuid

class LogAktivitas(Base):
    __tablename__ = "log_aktivitas"
    
    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    waktu = Column(DateTime, default=datetime.utcnow)
    aksi = Column(String, nullable=False)
    keterangan = Column(String, nullable=False)
    entitas = Column(String, nullable=False)
    id_entitas = Column(String, nullable=False)
    before_data = Column(JSON, nullable=False)
    after_data = Column(JSON, nullable=False)
    id_pengguna = Column(String, ForeignKey('pengguna.id', ondelete="CASCADE"), nullable=False)
    id_gudang = Column(String, ForeignKey("gudang.id", ondelete="CASCADE"), nullable=False)
    
    pengguna = relationship("Pengguna", back_populates="log_pengguna")
    gudang = relationship("Gudang", back_populates="log_gudang")