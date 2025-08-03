from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from enum import Enum

# Schema Transaksi 

# Enum untuk jenis transaksi
class JenisEnum(str, Enum):
    masuk = 'masuk'
    keluar = 'keluar'

# Base schema untuk Transaksi
class TransaksiBase(BaseModel):
    tanggal: date
    jenis: JenisEnum
    jumlah: int
    keterangan: str
    id_barang: str
    id_gudang: str

# Schema untuk operasi CRUD pada Transaksi
class TransaksiCreate(TransaksiBase):
    pass

class TransaksiUpdate(BaseModel):
    tanggal: Optional[date] = None
    jenis: Optional[JenisEnum] = None
    jumlah: Optional[int] = None
    keterangan: Optional[str] = None
    id_barang: Optional[str] = None
    id_gudang: Optional[str] = None

class TransaksiDelete(BaseModel):
    id: str

class TransaksiResponse(TransaksiBase):
    id: str
    model_config = ConfigDict(from_attributes=True)