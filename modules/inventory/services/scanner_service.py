import pytesseract
from PIL import Image
import requests
import json
import os
from dotenv import load_dotenv

from modules.inventory.services.barang_service import BarangService
from modules.inventory.schemas.barang_schema import BarangCreate
from modules.inventory.services.supplier_service import SupplierService
from modules.inventory.schemas.supplier_schema import SupplierCreate

from database.db import db

load_dotenv()

# Service untuk mengelola operasi bisnis pada pemindaian invoice

class ScannerService:
    # Metode statis untuk menyimpan data hasil pemindaian invoice
    @staticmethod
    def scan_invoice(path: str, id_gudang: str):
        # Menggunakan pytesseract untuk membaca teks dari gambar
        image = Image.open(path)
        text = pytesseract.image_to_string(image, lang="ind")
        
        # print(text)
        
        # Menggunakan OpenRouter API untuk memproses teks
        with open("configs/promp.txt", "r", encoding="utf-8") as file:
            context = file.read()
        
        # Mengambil API key dari environment variable
        API_KEY = os.getenv("OPENROUTER_KEY")
        
        # URL untuk OpenRouter API
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Headers untuk permintaan API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "X-Title": "MiniERP OCR Scanner"
        }
        
        # Data yang akan dikirim ke API
        # Menggunakan model GPT-3.5 Turbo
        data = {
            "model": "openai/gpt-3.5-turbo-0613",
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": text}
            ]
        }

        try:
            # Mengirim permintaan POST ke API
            response = requests.post(url, headers=headers, json=data)
            # Memeriksa apakah permintaan berhasil
            response.raise_for_status()
            # Mengambil hasil dari respons JSON
            result = response.json()

            # Memeriksa apakah ada pilihan dalam respons
            if "choices" in result and len(result["choices"]) > 0:
                # Mengambil konten dari pilihan pertama
                payload: str = str(result["choices"][0]["message"]["content"])
                # Mengonversi string JSON menjadi objek Python
                # Memanggil metode untuk menyimpan data
                ScannerService.save_data(json.loads(payload), id_gudang)
            else:
                print( "Error: Unexpected response structure")

        except requests.exceptions.RequestException as e:
            print( f"Request failed: {e}")
        except KeyError as e:
            print( f"Error processing response (KeyError): {e}")
        except json.JSONDecodeError as e:
            print( f"Error decoding JSON response: {e}")
        except Exception as e:
            print( f"An unexpected error occurred: {e}")
    
    # Metode statis untuk menyimpan data hasil pemindaian
    @staticmethod
    def save_data(data_scanner: json, id_gudang: str):
        # data_scanner = json.loads(ScannerService.scan_invoice(path))
        
        print(data_scanner)
        
        exist_supplier = SupplierService.get_all(db)
        
        for existing_supplier in exist_supplier:
            if existing_supplier.nama == data_scanner["supplier"]["nama"]:
                print(f"Supplier {existing_supplier.nama} already exists.")
                return
        
        # Mengambil data supplier dari hasil pemindaian
        supp = data_scanner["supplier"]
        
        if supp["telepon"] is None:
            telepon = "0"
        else: telepon = supp["telepon"]
        
        data_supplier = SupplierCreate(
            nama= supp["nama"],
            alamat=supp["alamat"],
            telepon= telepon,
            id_gudang=id_gudang
        )
        
        # print(data_supplier)
        # Menyimpan data supplier
        supplier = SupplierService.store(db, data_supplier)
        
        # Mengambil data barang dari hasil pemindaian
        for i, item in enumerate(data_scanner["items"], start=1):
            # Menggunakan format kode barang yang unik
            # Misalnya: BRG0001, BRG0002, dst.
            kd_barang = f"BRG{i:04d}"
            
            # Membuat objek BarangCreate dengan data yang diperlukan
            data_barang = BarangCreate(
                kd_barang=kd_barang,
                nama=item["nama_barang"],
                satuan=item["satuan"].lower(),
                stock=item["stock"],
                harga_beli=item["harga_beli"],
                harga_jual=None,
                id_kategori=None,
                id_supplier=supplier.id,
                id_gudang=id_gudang
            )
            
            BarangService.store(db, data_barang)
            # print(data_barang)