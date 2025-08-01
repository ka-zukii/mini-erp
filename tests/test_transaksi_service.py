import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base
from datetime import date

from modules.inventory.schemas.barang_schema import BarangCreate
from modules.inventory.schemas.gudang_schema import GudangCreate
from modules.inventory.schemas.transaksi_schema import TransaksiCreate, TransaksiUpdate
from modules.inventory.services.barang_service import BarangService
from modules.inventory.services.gudang_service import GudangService
from modules.inventory.services.transaksi_service import TransaksiService

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def init_gudang(db_session) -> str:
    gudang_data = GudangCreate(
        nama="Gudang A",
        lokasi="Jakarta",
        keterangan="Gudang Pusat"
    )
    
    gudang = GudangService.store(db_session, gudang_data)
    return gudang.id

def init_barang(db_session, id_gudang) -> str:
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
        id_gudang= id_gudang
    )
    
    barang = BarangService.store(db_session, barang_data)
    
    return barang.id

def test_create_and_get_transaksi(db_session):
    id_gudang = init_gudang(db_session)
    
    transaksi_data = TransaksiCreate(
        tanggal=date.today(),
        jenis='masuk',
        jumlah=10,
        keterangan='Barang masuk dari supplier',
        id_barang=init_barang(db_session, id_gudang),
        id_gudang=id_gudang
    )
    
    created = TransaksiService.store(db_session, transaksi_data)
    assert created.id is not None
    assert created.jenis == 'masuk'

def test_get_all_transaksi(db_session):
    id_gudang = init_gudang(db_session)
    
    transaksi_data1 = TransaksiCreate(
        tanggal=date.today(),
        jenis='masuk',
        jumlah=10,
        keterangan='Barang masuk dari supplier',
        id_barang=init_barang(db_session, id_gudang),
        id_gudang=id_gudang
    )
    
    transaksi_data2 = TransaksiCreate(
        tanggal=date.today(),
        jenis='keluar',
        jumlah=13,
        keterangan='Barang keluar dari supplier',
        id_barang=init_barang(db_session, id_gudang),
        id_gudang=id_gudang
    )
    
    TransaksiService.store(db_session, transaksi_data1)
    TransaksiService.store(db_session, transaksi_data2)
    
    list_data = TransaksiService.get_all(db_session)
    assert len(list_data) == 2

def test_update_transaksi(db_session):
    id_gudang = init_gudang(db_session)
    
    transaksi_data = TransaksiCreate(
        tanggal=date.today(),
        jenis='masuk',
        jumlah=10,
        keterangan='Barang masuk dari supplier',
        id_barang=init_barang(db_session, id_gudang),
        id_gudang=id_gudang
    )
    
    created = TransaksiService.store(db_session, transaksi_data)
    update_data = TransaksiUpdate(jenis='keluar')
    
    updated = TransaksiService.update(db_session, created.id, update_data)
    assert updated.jenis == 'keluar'

def test_delete_transaksi(db_session):
    id_gudang = init_gudang(db_session)
    
    transaksi_data = TransaksiCreate(
        tanggal=date.today(),
        jenis='masuk',
        jumlah=10,
        keterangan='Barang masuk dari supplier',
        id_barang=init_barang(db_session, id_gudang),
        id_gudang=id_gudang
    )
    
    created = TransaksiService.store(db_session, transaksi_data)
    
    result = TransaksiService.destroy(db_session, created.id)
    assert result is True
    
    assert TransaksiService.get_by_id(db_session, created.id) is None