from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base

from modules.inventory.schemas.gudang_schema import GudangCreate
from modules.inventory.schemas.pengguna_schema import PenggunaCreate
from modules.inventory.services.gudang_service import GudangService
from modules.inventory.services.log_aktivitas_service import LogAktivitasService
from modules.inventory.schemas.log_aktivitas_schema import LogAktivitasCreate, LogAktivitasUpdate
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

def init_gudang(db_session) -> str:
    gudang_data = GudangCreate(
        nama="Gudang A",
        lokasi="Jakarta",
        keterangan="Gudang Pusat"
    )
    
    gudang = GudangService.store(db_session, gudang_data)
    return gudang.id

def init_pengguna(db_session, id_gudang) -> str:
    pengguna_data = PenggunaCreate(
        nama_lengkap="Admin Andika",
        username="andikas",
        password="andikas",
        role="admin",
        refresh_token="a",
        sign_status=True,
        id_gudang=id_gudang
    )
    
    pengguna = PenggunaService.store(db_session, pengguna_data)
    return pengguna.id

def test_create_and_get_log_aktivitas(db_session):
    id_gudang = init_gudang(db_session)
    id_pengguna = init_pengguna(db_session, id_gudang)

    log_aktivitas_data = LogAktivitasCreate(
        waktu=datetime.now(),
        aksi="UPDATE",
        keterangan="Mengubah data pengguna",
        entitas="User",
        id_entitas="usr_12345",
        before_data={"nama": "Rizky", "email": "rizky@example.com"},
        after_data={"nama": "Andika", "email": "andika@example.com"},
        id_pengguna=id_pengguna,
        id_gudang=id_gudang
    )
    
    log_aktivitas = LogAktivitasService.store(db_session, log_aktivitas_data)
    assert log_aktivitas.id is not None
    assert log_aktivitas.aksi == "UPDATE"