from sqlalchemy.orm import Session
from modules.inventory.schemas.log_aktivitas_schema import LogAktivitasCreate, LogAktivitasUpdate
from modules.inventory.models import *

class LogAktivitasService:
    def get_all(db: Session):
        return db.query(LogAktivitas).all()
    
    def get_by_id(db: Session, id: str):
        return db.query(LogAktivitas).filter(LogAktivitas.id == id).first()
    
    def store(db: Session, data: LogAktivitasCreate):
        data_log_aktivitas = LogAktivitas(
            waktu = data.waktu,
            aksi = data.aksi,
            keterangan = data.keterangan,
            entitas = data.entitas,
            id_entitas = data.id_entitas,
            before_data = data.before_data,
            after_data = data.after_data,
            id_pengguna = data.id_pengguna,
            id_gudang = data.id_gudang
        )
        
        db.add(data_log_aktivitas)
        db.commit()
        db.refresh(data_log_aktivitas)
        return data_log_aktivitas
    
    # def update(db: Session, id: str, data: LogAktivitasUpdate):
    #     log_aktivitas = db.query(LogAktivitas).filter(LogAktivitas.id == id).first()
        
    #     if not log_aktivitas:
    #         return None
        
    #     for field, value in data.model_dump(exclude_unset=True).items():
    #         setattr(log_aktivitas, field, value)
        
    #     db.commit()
    #     db.refresh(log_aktivitas)
    #     return log_aktivitas
    
    # def destroy(db: Session, id: str):
    #     log_aktivitas = db.query(LogAktivitas).filter(LogAktivitas.id == id).first()
        
    #     if not log_aktivitas:
    #         return False
        
    #     db.delete(log_aktivitas)
    #     db.commit()
    #     return True