from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from cuid2 import Cuid
from dotenv import load_dotenv

load_dotenv()

# Getting database url from .env
DATABASE_URL= f'postgresql+psycopg2://{os.environ.get("DATABASE_URL")}'

# Make CUID
CUID_GENERATOR: Cuid = Cuid(length=10)

engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def generate_cuid():
    return CUID_GENERATOR.generate()