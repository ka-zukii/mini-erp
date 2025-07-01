import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base

from modules.inventory.schemas.gudang_schema import GudangCreate
from modules.inventory.services.gudang_service import GudangService
from modules.inventory.schemas.pengguna_schema import PenggunaCreate, PenggunaUpdate
from modules.inventory.services.pengguna_service import PenggunaService

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

def test_create_and_get_pengguna(db_session):
    pengguna_data = PenggunaCreate(
        nama_lengkap="Admin Andika",
        username="andikas",
        password="andikas",
        role="admin",
        refresh_token="a",
        sign_status=True,
        id_gudang=init_gudang(db_session)
    )
    
    created = PenggunaService.store(db_session, pengguna_data)
    assert created.id is not None
    assert created.nama_lengkap == "Admin Andika"
    assert created.role == "admin"

def test_get_all_pengguna(db_session):
    pengguna_data1 = PenggunaCreate(
        nama_lengkap="Admin Andika",
        username="andikas",
        password="andikas",
        role="admin",
        refresh_token="a",
        sign_status=True,
        id_gudang=init_gudang(db_session)
    )
    
    pengguna_data2 = PenggunaCreate(
        nama_lengkap="Admin Kazuki",
        username="kazuki",
        password="kazuki",
        role="user",
        refresh_token="aauwhduy",
        sign_status=False,
        id_gudang=init_gudang(db_session)
    )
    
    PenggunaService.store(db_session, pengguna_data1)
    PenggunaService.store(db_session, pengguna_data2)
    
    list_data = PenggunaService.get_all(db_session)
    assert len(list_data) == 2

def test_update_pengguna(db_session):
    pengguna_data = PenggunaCreate(
        nama_lengkap="Admin Andika",
        username="andikas",
        password="andikas",
        role="admin",
        refresh_token="a",
        sign_status=True,
        id_gudang=init_gudang(db_session)
    )
    
    created = PenggunaService.store(db_session, pengguna_data)
    update_data = PenggunaUpdate(nama_lengkap="Andika Sukma", sign_status=False)
    
    updated = PenggunaService.update(db_session, created.id, update_data)
    assert updated.nama_lengkap == "Andika Sukma"
    assert updated.sign_status == False

def test_delete_pengguna(db_session):
    pengguna_data = PenggunaCreate(
        nama_lengkap="Admin Andika",
        username="andikas",
        password="andikas",
        role="admin",
        refresh_token="a",
        sign_status=True,
        id_gudang=init_gudang(db_session)
    )
    
    created = PenggunaService.store(db_session, pengguna_data)
    
    result = PenggunaService.destroy(db_session, created.id)
    assert result is True
    
    assert PenggunaService.get_by_id(db_session, created.id) is None