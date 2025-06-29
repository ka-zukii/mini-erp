import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base
from modules.inventory.services.barang_service import BarangService
from modules.inventory.schemas.barang_schema import BarangCreate, BarangUpdate

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

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
        id_gudang="gudang1"
    )
    
    created = BarangService.store(db_session, barang_data)
    assert created.id is not None
    assert created.name == "Sabun Mandi"
    
    fetched = BarangService.get_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.kd_barang == "BRG001"