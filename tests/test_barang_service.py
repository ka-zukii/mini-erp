import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base

from modules.inventory.services.barang_service import BarangService
from modules.inventory.services.gudang_service import GudangService
from modules.inventory.schemas.barang_schema import BarangCreate, BarangUpdate
from modules.inventory.schemas.gudang_schema import GudangCreate

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def init_gudang(db_session):
    gudang_data = GudangCreate(
        nama="Gudang A",
        lokasi="Jakarta",
        keterangan="Gudang Pusat"
    )
    
    gudang = GudangService.store(db_session, gudang_data)
    
    return gudang.id

def test_create_and_get_barang(db_session):
    barang_data = BarangCreate(
        kd_barang="BRG001",
        nama="Sabun Mandi",
        deskripsi="Sabun mandi batang 100gram",
        satuan="pcs",
        harga_beli=5000,
        harga_jual=7000,
        stock=20,
        id_kategori=None,
        id_supplier=None,
        id_gudang= init_gudang(db_session)
    )
    
    created = BarangService.store(db_session, barang_data)
    assert created.id is not None
    assert created.nama == "Sabun Mandi"
    
    fetched = BarangService.get_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.kd_barang == "BRG001"

def test_get_all_barang(db_session):
    barang_data1 = BarangCreate(
        kd_barang="BRG001",
        nama="Sabun Muka",
        deskripsi="Sabun muka 1liter",
        satuan="pcs",
        harga_beli=5000,
        harga_jual=7000,
        stock=20,
        id_kategori=None,
        id_supplier=None,
        id_gudang=init_gudang(db_session)
    )
    
    barang_data2 = BarangCreate(
        kd_barang="BRG002",
        nama="Sikat Gigi",
        deskripsi="Sikat gigi bulu lembut",
        satuan="pcs",
        harga_beli=10000,
        harga_jual=12000,
        stock=10,
        id_kategori=None,
        id_supplier=None,
        id_gudang=init_gudang(db_session)
    )
    
    BarangService.store(db_session, barang_data1)
    BarangService.store(db_session, barang_data2)
    
    list_data = BarangService.get_all(db_session)
    assert len(list_data) == 2

def test_update_barang(db_session):
    barang_data = BarangCreate(
        kd_barang="BRG001",
        nama="Sabun Mandi",
        deskripsi="Sabun mandi batang 100gram",
        satuan="pcs",
        harga_beli=5000,
        harga_jual=7000,
        stock=20,
        id_kategori=None,
        id_supplier=None,
        id_gudang= init_gudang(db_session)
    )
    
    created = BarangService.store(db_session, barang_data)
    update_data = BarangUpdate(nama="Sabun Muka", stock=50)
    
    updated = BarangService.update(db_session, created.id, update_data)
    assert updated.nama == "Sabun Muka"
    assert updated.stock == 50
    
def test_delete_barang(db_session):
    barang_data = BarangCreate(
        kd_barang="BRG001",
        nama="Sabun Mandi",
        deskripsi="Sabun mandi batang 100gram",
        satuan="pcs",
        harga_beli=5000,
        harga_jual=7000,
        stock=20,
        id_kategori=None,
        id_supplier=None,
        id_gudang= init_gudang(db_session)
    )
    
    created = BarangService.store(db_session, barang_data)
    
    result = BarangService.destroy(db_session, created.id)
    assert result is True
    
    assert BarangService.get_by_id(db_session, created.id) is None