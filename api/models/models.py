from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONN = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_CONN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine) #Tabloları oluşturmak için.

"""
Veri tabanı bağlantısının çalışıp çalışmadığını denedim:
try:
    with engine.connect() as connection:
        print("Veritabanına başarıyla bağlandı!")
except Exception as e:
    print(f"Veritabanına bağlanırken hata oluştu: {e}")
"""

def get_db(): #Veri tabanı için session oluşturulur.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(String(5000), nullable=False)
    chatbot_response = Column(String(5000), nullable=False)
    session_id = Column(String(50), nullable=False)
    datetime = Column(DateTime(timezone=True), server_default=func.now())