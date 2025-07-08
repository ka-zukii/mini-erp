import pytest

from modules.inventory.services.scanner_service import ScannerService

@pytest.fixture(scope="function")
def test_scanner():
    text = ScannerService.scan_one()
    assert text is not ""