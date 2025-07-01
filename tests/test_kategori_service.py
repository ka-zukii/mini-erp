import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base

from modules.inventory.schemas.gudang_schema import GudangCreate
from modules.inventory.services.gudang_service import GudangService
from modules.inventory.services.kategori_service import KategoriService
from modules.inventory.schemas.kategori_schema import KategoriCreate, KategoriUpdate


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

def test_create_and_get_kategori(db_session):
    kategori_data = KategoriCreate(
        nama="ATK",
        deskripsi="Alat Tulis Kantor",
        id_gudang=init_gudang(db_session)
    )
    
    created = KategoriService.store(db_session, kategori_data)
    assert created.id is not None
    assert created.nama == "ATK"
    
    fetched = KategoriService.get_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.nama == "ATK"
    assert fetched.deskripsi == "Alat Tulis Kantor"

def test_get_all_kategori(db_session):
    kategori_data1 = KategoriCreate(
        nama="ATK",
        deskripsi="Alat Tulis Kantor",
        id_gudang=init_gudang(db_session)
    )
    
    kategori_data2 = KategoriCreate(
        nama="Komputer",
        deskripsi="Khusus peralatan komputer",
        id_gudang=init_gudang(db_session)
    )
    
    KategoriService.store(db_session, kategori_data1)
    KategoriService.store(db_session, kategori_data2)
    
    list_data = KategoriService.get_all(db_session)
    assert len(list_data) == 2

def test_update_kategori(db_session):
    kategori_data = KategoriCreate(
        nama="Mebel",
        deskripsi="Mbel",
        id_gudang=init_gudang(db_session)
    )
    
    created = KategoriService.store(db_session, kategori_data)
    update_data = KategoriUpdate(nama="KBH", deskripsi="Kebersihan")
    
    updated = KategoriService.update(db_session, created.id, update_data)
    assert updated.nama == "KBH"
    assert updated.deskripsi == "Kebersihan"

def test_delete_kategori(db_session):
    kategori_data = KategoriCreate(
        nama="ATK",
        deskripsi= "Alat Tulis Kantor" ,
        id_gudang=init_gudang(db_session)
    )
    
    created = KategoriService.store(db_session, kategori_data)
    
    result = KategoriService.destroy(db_session, created.id)
    assert result is True
    
    assert KategoriService.get_by_id(db_session, created.id) is None