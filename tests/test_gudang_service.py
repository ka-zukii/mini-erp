import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base
from modules.inventory.services.gudang_service import GudangService
from modules.inventory.schemas.gudang_schema import GudangCreate, GudangUpdate

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_gudang(db_session):
    gudang_data = GudangCreate(
        nama="Gudang Surakarta",
        lokasi="Surakarta",
        keterangan="Gudang penyimpanan barang di Surakarta"
    )
    
    created = GudangService.store(db_session, gudang_data)
    assert created.id is not None
    assert created.nama == "Gudang Surakarta"
    
    fetched = GudangService.get_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.nama == "Gudang Surakarta"

def test_get_all_gudang(db_session):
    gudang_data1 = GudangCreate(
        nama="Gudang ATK",
        lokasi="Surakarta",
        keterangan="Gudang penyimpanan ATK"
    )
    
    gudang_data2 = GudangCreate(
        nama="Gudang Mebel",
        lokasi="Jakarta",
        keterangan="Gudang penyimpanan mebel"
    )
    
    GudangService.store(db_session, gudang_data1)
    GudangService.store(db_session, gudang_data2)
    
    list_data = GudangService.get_all(db_session)
    assert len(list_data) == 2

def test_update_gudang(db_session):
    gudang_data = GudangCreate(
        nama="Gudang Surakarta",
        lokasi="Surakarta",
        keterangan="Gudang penyimpanan barang di Surakarta"
    )
    
    created = GudangService.store(db_session, gudang_data)
    update_data = GudangUpdate(nama="Gudang ATK", lokasi="Surakarta")
    
    updated = GudangService.update(db_session, created.id, update_data)
    assert updated.nama == "Gudang ATK"
    assert updated.lokasi == "Surakarta"

def test_delete_gudang(db_session):
    gudang_data = GudangCreate(
        nama="Gudang Surakarta",
        lokasi="Surakarta",
        keterangan="Gudang penyimpanan barang di Surakarta"
    )
    
    created = GudangService.store(db_session, gudang_data)
    
    result = GudangService.destroy(db_session, created.id)
    assert result is True
    
    assert GudangService.get_by_id(db_session, created.id) is None