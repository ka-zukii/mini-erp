import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base

from modules.inventory.schemas.gudang_schema import GudangCreate
from modules.inventory.schemas.supplier_schema import SupplierCreate, SupplierUpdate
from modules.inventory.services.gudang_service import GudangService
from modules.inventory.services.supplier_service import SupplierService

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

def test_create_and_get_supplier(db_session):
    supplier_data = SupplierCreate(
        nama="Jokonis",
        telepon="085161742553",
        alamat="Surakarta ngidul sitik"
    )
    
    created = SupplierService.store(db_session, supplier_data)
    assert created.id is not None
    assert created.nama == "Jokonis"
    
    fetched = SupplierService.get_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.nama == "Jokonis"

def test_get_all_supplier(db_session):
    supplier_data1 = SupplierCreate(
        nama="Jokonis",
        telepon="085161742553",
        alamat="Surakarta ngidul sitik"
    )
    
    supplier_data2 = SupplierCreate(
        nama="Bowonis",
        telepon="085161742553",
        alamat="Surakarta ngidul sitik"
    )
    
    SupplierService.store(db_session, supplier_data1)
    SupplierService.store(db_session, supplier_data2)
    
    list_data = SupplierService.get_all(db_session)
    assert len(list_data) == 2

def test_update_supplier(db_session):
    supplier_data = SupplierCreate(
        nama="Jokonis",
        telepon="085161742553",
        alamat="Surakarta ngidul sitik"
    )
    
    created = SupplierService.store(db_session, supplier_data)
    update_data = SupplierUpdate(nama="Adonis")
    
    updated = SupplierService.update(db_session, created.id, update_data)
    assert updated.nama == "Adonis"

def test_delete_supplier(db_session):
    supplier_data = SupplierCreate(
        nama="Jokonis",
        telepon="085161742553",
        alamat="Surakarta ngidul sitik"
    )
    
    created = SupplierService.store(db_session, supplier_data)
    
    result = SupplierService.destroy(db_session, created.id)
    assert result is True
    
    assert SupplierService.get_by_id(db_session, created.id) is None