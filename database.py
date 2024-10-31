import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# for docker use
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@host.docker.internal:5432/postgres"

# for local use
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/postgres"

db_user = os.getenv('DB_USERNAME')
if db_user is None:
    db_user = 'rhushi'

db_pass = os.getenv('DB_PASSWORD')
if db_pass is None:
    db_pass = 123

db_host = os.getenv('DB_HOST')
if db_host is None:
    db_host = 'localhost'

db_port = os.getenv('DB_PORT')
if db_port is None:
    db_port = 5432

db_schema = os.getenv('DB_SCHEMA')
if db_schema is None:
    db_schema = 'postgres'

# for use with Kubernetes use this url
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_schema}"
# Use your database URL here
print("DB URL",SQLALCHEMY_DATABASE_URL)

#SQLALCHEMY_DATABASE_URL = "postgresql://rhushi:123@host.docker.internal/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
