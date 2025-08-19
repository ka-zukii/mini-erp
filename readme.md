# PROJECT STILL ON DEVELOPMENT!!!

## Setup Project Python

Membuat virtual environment (opsional tapi disarankan):

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate   # Windows
```

Install dependensi yang diperlukan:

```bash
pip install -r requirements.txt
```

## Database Migration Guide

### 1. Konfigurasi .env

Rubah file .env.example menjadi .env lalu pada nilai DATABASE_URL dirubah menggunakan URL Database yang anda miliki. 

Noted: Proyek ini menggunakan PostgreeSQL sebagai database utama.

### 2. Buat Migration Baru (Initial Migration)

Jalankan perintah berikut untuk membuat file migration berdasarkan perubahan pada models:

```bash
alembic revision --autogenerate -m "initial"
```

### 3. Terapkan Migration ke Database (Push Migration)

Setelah file migration dibuat, jalankan perintah ini untuk menerapkan perubahan ke database:

```bash
alembic upgrade head
```
Noted: Jika terjadi error pada saat menjalankan migration. jika didalam directory alembic/ tidak terdapat directory versions, anda harus membuatnya terlebih dahulu.
