from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Database එකට connect වෙන URL එක (Mac එකේ local database එකට)
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://localhost/autorescue_db"


# Engine එකක් හදනවා (මේකෙන් තමයි DB එකට කතා කරන්නේ)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session එකක් හදනවා (දත්ත දාන්න, ගන්න පාවිච්චි කරන්නේ මේක)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tables හදන්න පාවිච්චි කරන Base class එක
Base = declarative_base()
