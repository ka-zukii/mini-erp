import pytesseract
from PIL import Image
import requests
import json
import os
from dotenv import load_dotenv

from modules.inventory.services.barang_service import BarangService
from modules.inventory.schemas.barang_schema import BarangCreate

load_dotenv()

class ScannerService:
    API_KEY = os.getenv("OPENROUTER_KEY")

    @staticmethod
    def ocr(path: str) -> str:
        image = Image.open(path)
        text = pytesseract.image_to_string(image, lang="ind")
        
        # print(text)

        with open("configs/promp.txt", "r", encoding="utf-8") as file:
            context = file.read()

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {ScannerService.API_KEY}",
            "Content-Type": "application/json",
            "X-Title": "MiniERP OCR Scanner"
        }

        data = {
            "model": "openai/gpt-3.5-turbo-0613",
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": text}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "Error: Unexpected response structure"

        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"
        except KeyError as e:
            return f"Error processing response (KeyError): {e}"
        except json.JSONDecodeError as e:
            return f"Error decoding JSON response: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    
    def scan_barang(path: str):
        data_scanner = json.loads(ScannerService.ocr(path))
        
        # print(data_scanner)
        
        for i, item in enumerate(data_scanner["items"], start=1):
            kd_barang = f"BRG{i:04d}"
            
            data_barang = BarangCreate(
                kd_barang=kd_barang,
                nama=item["nama_barang"],
                satuan=item["satuan"].lower(),
                stock=item["stock"],
                harga_beli=item["harga_beli"],
                harga_jual=None,
                id_kategori=None,
                id_supplier=None,
                id_gudang="GD1"
            )
            
            print(data_barang)