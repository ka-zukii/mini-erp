from pydantic import BaseModel, ConfigDict
from typing import Optional, Union, Dict, Any, List
from datetime import datetime

class LogAktivitasBase(BaseModel):
    waktu: datetime
    aksi: str
    keterangan: str
    entitas: str
    id_entitas: str
    before_data: Optional[Union[Dict[str, Any], List[Any]]] = None
    after_data: Optional[Union[Dict[str, Any], List[Any]]] = None
    id_pengguna: str
    id_gudang: str

class LogAktivitasCreate(LogAktivitasBase):
    pass

class LogAktivitasUpdate(BaseModel):
    waktu: Optional[datetime] = None
    aksi: Optional[str] = None
    keterangan: Optional[str] = None
    entitas: Optional[str] = None
    id_entitas: Optional[str] = None
    before_data: Optional[Union[Dict[str, Any], List[Any]]] = None
    after_data: Optional[Union[Dict[str, Any], List[Any]]] = None
    id_pengguna: Optional[str] = None
    id_gudang: Optional[str] = None

class LogAktivitasDelete(BaseModel):
    id: str

class LogAktivitasResponse(LogAktivitasBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)