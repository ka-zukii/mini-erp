from pydantic import BaseModel, ConfigDict
from typing import Optional

class GudangBase(BaseModel):
    nama: str
    lokasi: str
    keterangan: str

class GudangCreate(GudangBase):
    pass

class GudangUpdate(BaseModel):
    nama: Optional[str] = None
    lokasi: Optional[str] = None
    keterangan: Optional[str] = None

class GudangDelete(BaseModel):
    id:str

class GudangResponse(GudangBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)
