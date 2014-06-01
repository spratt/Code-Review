from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()

class Code(Base):
    __tablename__ = 'code'
    
    id = Column(Integer, Sequence('code_id_seq'), primary_key=True)
    text = Column(String)
    lang = Column(String)
