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
    def save_data(data_scanner: dict, id_gudang: str):
        # Debug log
        print(f"[DEBUG] Data hasil scanner:\n{data_scanner}")

        # Ambil semua supplier yang sudah ada
        existing_suppliers = SupplierService.get_all(db)

        # Cek apakah supplier sudah ada berdasarkan nama
        scanned_supplier = data_scanner["supplier"]
        matching_supplier = next(
            (s for s in existing_suppliers if s.nama.lower() == scanned_supplier["nama"].lower()),
            None
        )

        if matching_supplier:
            print(f"Supplier '{matching_supplier.nama}' sudah ada.")
            supplier = matching_supplier
        else:
            # Normalisasi data supplier
            telepon = scanned_supplier.get("telepon") or "0"

            # Simpan supplier baru
            data_supplier = SupplierCreate(
                nama=scanned_supplier["nama"],
                alamat=scanned_supplier["alamat"],
                telepon=telepon,
                id_gudang=id_gudang
            )
            supplier = SupplierService.store(db, data_supplier)
            print(f"Supplier '{supplier.nama}' berhasil disimpan.")

        # Ambil semua barang yang sudah ada
        existing_items = BarangService.get_all(db)

        for i, item in enumerate(data_scanner["items"], start=1):
            # Cek apakah barang sudah ada berdasarkan nama + supplier + gudang
            duplicate = next(
                (b for b in existing_items
                if b.nama.lower() == item["nama_barang"].lower()
                and b.id_supplier == supplier.id
                and b.id_gudang == id_gudang),
                None
            )

            if duplicate:
                print(f"Barang '{item['nama_barang']}' dari supplier ini sudah ada. Lewati.")
                continue  # Lewati jika duplikat

            # Generate kode barang unik
            kd_barang = f"BRG{i:04d}"

            # Simpan barang baru
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
            print(f"Barang '{item['nama_barang']}' berhasil disimpan.")