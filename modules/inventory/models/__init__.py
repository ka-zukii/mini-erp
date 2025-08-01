from .barang import Barang
from .gudang import Gudang
from .kategori import Kategori
from .supplier import Supplier
from .transaksi import Transaksi

# Trigger semua model ter-load ke dalam registry SQLAlchemy
__all__ = [
    "Barang",
    "Gudang",
    "Kategori",
    "Supplier",
    "Transaksi",
]