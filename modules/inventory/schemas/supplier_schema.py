from pydantic import BaseModel, ConfigDict
from typing import Optional

class SupplierBase(BaseModel):
    nama: str
    telepon: str
    alamat: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    nama: Optional[str] = None
    telepon: Optional[str] = None
    alamat: Optional[str] = None

class SupplierDelete(BaseModel):
    id: str

class SupplierResponse(SupplierBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)