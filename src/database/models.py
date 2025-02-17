from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FlatFileData(Base):
    __tablename__ = "flat_file_data"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
    source_type = Column(String(50))
    status = Column(String(20), default="raw")

    def __repr__(self):
        return f"<FlatFileData(filename='{self.filename}', processed_at='{self.processed_at}')>" 