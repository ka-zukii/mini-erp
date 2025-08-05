from sqlalchemy.orm import Session
from modules.inventory.models import Gudang, Barang, Transaksi
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import pandas as pd

class ExcelService:
    @staticmethod
    def export_barang(db: Session):
        root = Tk()
        root.withdraw()
        file_path = asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Simpan File Excel",
            initialfile="laporan_gudang.xlsx"
        )
        root.destroy()

        if not file_path:
            print("⚠️ Export dibatalkan.")
            return

        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                ada_data = False

                ada_data |= ExcelService.get_data_gudang(db, writer)
                ada_data |= ExcelService.get_data_barang_per_gudang(db, writer)
                ada_data |= ExcelService.get_data_transaksi_per_gudang(db, writer)
                ada_data |= ExcelService.get_laporan_keuangan(db, writer)

                if not ada_data:
                    # Buat sheet kosong untuk menghindari error
                    pd.DataFrame([{"Info": "Tidak ada data"}]).to_excel(writer, index=False, sheet_name="Info")

            print("✅ Berhasil mengekspor data ke Excel.")
        except Exception as e:
            print(f"❌ Terjadi kesalahan saat mengekspor data: {e}")
        finally:
            db.close()

    @staticmethod
    def get_data_gudang(db: Session, writer: pd.ExcelWriter) -> bool:
        gudang_list = db.query(Gudang).all()
        data_gudang = [{
            "ID Gudang": g.id,
            "Nama Gudang": g.nama,
            "Lokasi": g.lokasi,
            "Keterangan": g.keterangan
        } for g in gudang_list]

        df = pd.DataFrame(data_gudang)
        if df.empty:
            return False

        df.to_excel(writer, index=False, sheet_name='Daftar Gudang')
        return True

    @staticmethod
    def get_data_barang_per_gudang(db: Session, writer: pd.ExcelWriter) -> bool:
        ada_data = False
        gudang_list = db.query(Gudang).all()

        for gudang in gudang_list:
            barang_list = db.query(Barang).filter(Barang.id_gudang == gudang.id).all()

            data = [{
                "ID Barang": b.id,
                "Kode Barang": b.kd_barang,
                "Nama Barang": b.nama,
                "Kategori": b.kategori.nama if b.kategori else "",
                "Supplier": b.supplier.nama if b.supplier else "",
                "Deskripsi": b.deskripsi,
                "Satuan": b.satuan,
                "Harga Beli": float(b.harga_beli),
                "Harga Jual": float(b.harga_jual) if b.harga_jual else 0,
                "Stok": b.stock
            } for b in barang_list]

            df = pd.DataFrame(data)
            if df.empty:
                continue

            sheet_name = f"Barang - {gudang.nama[:25]}" if gudang.nama else f"Barang - {gudang.id}"
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            ada_data = True

        return ada_data

    @staticmethod
    def get_data_transaksi_per_gudang(db: Session, writer: pd.ExcelWriter) -> bool:
        ada_data = False
        gudang_list = db.query(Gudang).all()

        for gudang in gudang_list:
            transaksi_list = db.query(Transaksi).filter(Transaksi.id_gudang == gudang.id).all()

            data = [{
                "ID Transaksi": t.id,
                "Tanggal": t.tanggal,
                "Jenis": t.jenis,
                "Jumlah": t.jumlah,
                "Barang": t.barang.nama if t.barang else "",
                "Harga Beli": float(t.barang.harga_beli) if t.barang else 0,
                "Harga Jual": float(t.barang.harga_jual) if t.barang and t.barang.harga_jual else 0,
                "Keterangan": t.keterangan or ""
            } for t in transaksi_list]

            df = pd.DataFrame(data)
            if df.empty:
                continue

            sheet_name = f"Transaksi - {gudang.nama[:25]}" if gudang.nama else f"Transaksi - {gudang.id}"
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            ada_data = True

        return ada_data

    @staticmethod
    def get_laporan_keuangan(db: Session, writer: pd.ExcelWriter) -> bool:
        transaksi_list = db.query(Transaksi).all()
        if not transaksi_list:
            return False

        data_laporan = []
        total_masuk = 0
        total_keluar = 0

        for t in transaksi_list:
            if not t.barang:
                continue
            harga = float(t.barang.harga_beli if t.jenis == 'masuk' else t.barang.harga_jual or 0)
            total = harga * t.jumlah
            data_laporan.append({
                "Tanggal": t.tanggal,
                "Jenis": t.jenis,
                "Barang": t.barang.nama,
                "Jumlah": t.jumlah,
                "Harga Satuan": harga,
                "Total": total
            })
            if t.jenis == 'masuk':
                total_masuk += total
            else:
                total_keluar += total

        df_laporan = pd.DataFrame(data_laporan)
        if df_laporan.empty:
            return False

        df_laporan.to_excel(writer, index=False, sheet_name="Laporan Keuangan")

        # Ringkasan
        df_ringkasan = pd.DataFrame([
            {"Keterangan": "Total Pembelian", "Total": total_masuk},
            {"Keterangan": "Total Penjualan", "Total": total_keluar},
            {"Keterangan": "Laba / Rugi", "Total": total_keluar - total_masuk}
        ])
        df_ringkasan.to_excel(writer, index=False, sheet_name="Ringkasan Keuangan")
        return True