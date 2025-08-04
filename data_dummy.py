dummy_warehouse_list = [
    ["G001", "Gudang Utama", "Gudang pusat untuk seluruh stok utama", "Jakarta"],
    ["G002", "Gudang Cabang A", "Gudang cabang wilayah timur", "Surabaya"],
    ["G003", "Gudang Cabang B", "Gudang cabang wilayah barat", "Bandung"],
    ["G004", "Gudang Cadangan", "Gudang untuk penyimpanan sementara", "Yogyakarta"],
    ["G005", "Gudang Online", "Khusus pesanan online dan e-commerce", "Depok"]
]

dummy_stock = {
    "G001": [
        [1, "BRG001", "Pensil", "PCS", 1000, 1500, 50, "Alat tulis"],
        [2, "BRG002", "Buku Tulis", "PCS", 3000, 5000, 100, "40 lembar"],
        [3, "BRG003", "Penghapus", "PCS", 500, 800, 75, "Karet"],
        [4, "BRG004", "Pulpen", "PCS", 2000, 3500, 40, "Tinta biru"],
        [5, "BRG005", "Spidol", "PCS", 2500, 4000, 60, "Permanent"]
    ],
    "G002": [
        [1, "BRG006", "Kertas A4", "RIM", 20000, 25000, 30, "Putih polos"],
        [2, "BRG007", "Stabilo", "PCS", 1500, 2500, 45, "Warna warni"],
        [3, "BRG008", "Lakban", "PCS", 1000, 1700, 20, "Coklat"],
        [4, "BRG009", "Amplop", "PCS", 300, 500, 100, "Kecil"],
        [5, "BRG010", "Binder", "PCS", 4000, 6000, 25, "Warna hitam"]
    ]
}

dummy_supplier = {
    "G001": [
        [1, 1, "PT Pena", "08123456789", "Jl. Pena Raya"],
        [2, 2, "PT Kertas Tulis", "08234567890", "Jl. Buku Tulis No.2"],
        [3, 3, "CV Eraser", "08345678901", "Jl. Penghapus Indah"],
        [4, 4, "Pulpen Corp", "08456789012", "Jl. Tinta Hitam"],
        [5, 5, "Spidol Inc", "08567890123", "Jl. Spidol City"]
    ],
    "G002": [
        [1, 1, "Kertas A4 Co", "08999999999", "Jl. Kertas Raya"],
        [2, 2, "Stabilo Bright", "08888888888", "Jl. Warna Cerah"],
        [3, 3, "Lakban Sejati", "08777777777", "Jl. Kuat No. 1"],
        [4, 4, "Amplop Aman", "08666666666", "Jl. Surat Masuk"],
        [5, 5, "Binder Books", "08555555555", "Jl. Arsip Tersimpan"]
    ]
}

dummy_transaction = {
    "G001": [
        [1, 1, "G001", "2025-08-01", "IN", 10, "Restock"],
        [2, 2, "G001", "2025-08-01", "OUT", 5, "Penjualan"],
        [3, 3, "G001", "2025-08-02", "IN", 15, "Restock"],
        [4, 4, "G001", "2025-08-03", "OUT", 10, "Penjualan"],
        [5, 5, "G001", "2025-08-04", "IN", 20, "Pembelian"]
    ],
    "G002": [
        [1, 1, "G002", "2025-08-01", "IN", 30, "Restock"],
        [2, 2, "G002", "2025-08-01", "OUT", 15, "Penjualan"],
        [3, 3, "G002", "2025-08-02", "IN", 20, "Pembelian"],
        [4, 4, "G002", "2025-08-03", "OUT", 25, "Distribusi"],
        [5, 5, "G002", "2025-08-04", "IN", 10, "Penyesuaian"]
    ]
}

dummy_category = {
    "G001": [
        [1, "G001", "Alat Tulis", "Perlengkapan kantor"],
        [2, "G001", "Aksesoris", "Barang pelengkap"],
        [3, "G001", "Elektronik", "Barang elektronik ringan"],
        [4, "G001", "Kantor", "Barang kantor"],
        [5, "G001", "Arsip", "Kebutuhan dokumentasi"]
    ],
    "G002": [
        [1, "G002", "Dokumentasi", "Penyimpanan file"],
        [2, "G002", "Distribusi", "Pengemasan & pengiriman"],
        [3, "G002", "Kertas", "Semua jenis kertas"],
        [4, "G002", "Alat Tulis", "Pulpen, pensil, dll"],
        [5, "G002", "Aksesoris", "Barang pendukung"]
    ]
}
