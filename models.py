from sqlalchemy import Column, Integer, String, Float
from database import Base

# Database එකේ හැදෙන Mechanics Table එක
class Mechanic(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skill = Column(String)
    distance = Column(Float) # කිලෝමීටර් ගාණ (උදා: 2.5) දශම සංඛ්‍යාවක් විදිහට
