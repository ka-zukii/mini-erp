from pydantic import BaseModel, ConfigDict
from typing import Optional

class KategoriBase(BaseModel):
    nama: str
    deskripsi: str
    id_gudang: str

class KategoriCreate(KategoriBase):
    pass

class KategoriUpdate(BaseModel):
    nama: Optional[str] = None
    deskripsi: Optional[str] = None

class KategoriDelete(BaseModel):
    id: str

class KategoriResponse(KategoriBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)