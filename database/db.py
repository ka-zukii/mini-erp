from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from cuid2 import Cuid
from dotenv import load_dotenv

load_dotenv()

# Memdaftarkan URL database
DATABASE_URL= f'postgresql+psycopg2://{os.environ.get("DATABASE_URL")}'

# Membuat generator CUID
CUID_GENERATOR: Cuid = Cuid(length=10)

# Membuat koneksi ke database
engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Membuat sesi lokal
db = local_session()

# Membuat base untuk model
Base = declarative_base()

# Fungsi untuk membuat CUID
def generate_cuid():
    return CUID_GENERATOR.generate()