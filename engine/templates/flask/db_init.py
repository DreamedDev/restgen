from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


def create_db(db_uri):
    engine = create_engine(db_uri)
    if not database_exists(engine.url):
        create_database(engine.url)

