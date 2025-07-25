#mysql db engine and session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:redhat@localhost/expense_tracker_db"     #build connection string for mysql

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)      #sessionmaker for db operations
Base = declarative_base()