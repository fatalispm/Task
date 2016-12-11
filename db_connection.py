from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

DATABASE_NAME = "postgres"
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "beaver1"
DATABASE_HOST = "localhost"
Base = automap_base()
engine = create_engine(
    "postgres://%s:%s@%s/%s" %
    (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME))
Base.prepare(engine, reflect=True)

Persons = Base.classes.persons


def create_session():
    engine.dispose()
    Session = sessionmaker(bind=engine)
    return Session()
