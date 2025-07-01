from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class PenggunaBase(BaseModel):
    nama_lengkap: str
    username: str
    password: str
    role: RoleEnum
    refresh_token: str
    sign_status: bool
    id_gudang: str

class PenggunaCreate(PenggunaBase):
    pass

class PenggunaUpdate(BaseModel):
    nama_lengkap: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None
    refresh_token: Optional[str] = None
    sign_status: Optional[bool] = None
    id_gudang: Optional[str] = None

class PenggunaDelete(BaseModel):
    id: str

class PenggunaResponse(PenggunaBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)