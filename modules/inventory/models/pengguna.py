from sqlalchemy import Column, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base, generate_cuid

class Pengguna(Base):
    __tablename__ = "pengguna"

    id = Column(String, primary_key=True, index=True, default=generate_cuid)
    nama_lengkap = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum('user', 'admin', name='role_enum'), default='user', nullable=False)
    refresh_token = Column(String, nullable=True)
    sign_status = Column(Boolean, nullable=False)
    id_gudang = Column(String, ForeignKey('gudang.id', ondelete="CASCADE"))
    
    gudang = relationship('Gudang', back_populates='pengguna_list')
    log_pengguna = relationship("LogAktivitas", back_populates="pengguna", cascade="all, delete")