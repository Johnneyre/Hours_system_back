from fastapi import FastAPI
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

app = FastAPI()

Base = declarative_base()

# Database configuration
DATABASE_URL = f"postgresql://{env_vars['DB_USER']}:{env_vars['DB_PASSWORD']}@{env_vars['DB_HOST']}:{env_vars['DB_PORT']}/{env_vars['DB_NAME']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)