# PROJECT STILL ON DEVELOPMENT!!!

## Setup Project Python

Pastikan kamu sudah menginstall dependensi yang diperlukan:

```bash
pip install -r requirements.txt
```

Jika belum ada environment, kamu bisa membuat virtual environment terlebih dahulu (opsional tapi disarankan):

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate   # Windows
```

## Database Migration Guide

### 1. Buat Migration Baru (Initial Migration)

Jalankan perintah berikut untuk membuat file migration berdasarkan perubahan pada models:

```bash
alembic revision --autogenerate -m "initial"
```

### 2. Terapkan Migration ke Database (Push Migration)

Setelah file migration dibuat, jalankan perintah ini untuk menerapkan perubahan ke database:

```bash
alembic upgrade head
```
