from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from decimal import Decimal

# Enum Satuan
class SatuanEnum(str, Enum):
    pcs = "pcs"
    kg = "kg"
    liter = "liter"

class BarangBase(BaseModel):
    kd_barang: str
    nama: str
    deskripsi: Optional[str] = None
    satuan: str
    harga_beli: Decimal
    harga_jual: Optional[Decimal] = None
    stock: int
    id_kategori: Optional[str]
    id_gudang: str

class BarangCreate(BarangBase):
    pass

class BarangUpdate(BaseModel):
    nama: Optional[str] = None
    deskripsi: Optional[str] = None
    satuan: Optional[SatuanEnum] = None
    harga_beli: Optional[Decimal] = None
    harga_jual: Optional[Decimal] = None
    stock: Optional[int] = None
    id_kategori: Optional[str] = None

class BarangDelete(BaseModel):
    id:str

class BarangResponse(BarangBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)