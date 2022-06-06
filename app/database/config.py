from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///dev_database.sqlite"
# DATABASE_URL = "postgresql://fastapi_user:admin@localhost:5432/followthem_db"
database = Database(DATABASE_URL)
sqlalchemy_engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=sqlalchemy_engine)

session = Session()


def get_database() -> Database:
    return database
