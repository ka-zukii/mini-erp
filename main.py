from modules.inventory.services.scanner_service import ScannerService

def app():
    print(ScannerService.scan_one())

if __name__ == "__main__":
    app()