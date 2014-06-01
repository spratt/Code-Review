from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, Sequence('comment_id_seq'), primary_key=True)
    code_id = Column(String)
    text = Column(String)
    line_start = Column(Integer)
    line_end = Column(Integer)
    diffs = Column(String)

    def getDict(self):
        return {
            'id' : int(self.id),
            'code_id' : str(self.code_id),
            'text' : str(self.text),
            'line_start' : int(self.line_start),
            'line_end' : int(self.line_end),
            'diffs' : str(self.diffs)
        }
