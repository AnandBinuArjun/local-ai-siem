from sqlalchemy import create_engine, Column, String, Integer, Float, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class EventModel(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(Float, index=True)
    host = Column(String, index=True)
    source = Column(String, index=True)
    category = Column(String, index=True)
    subtype = Column(String)
    severity = Column(Integer)
    principal = Column(String, index=True)
    object = Column(String)
    fields = Column(JSON)
    raw = Column(Text)

class Database:
    def __init__(self, db_url="sqlite:///./aisiem.db"):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def init_db(self):
        Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Global instance
db_instance = Database()
