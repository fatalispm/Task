from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm.session import sessionmaker
from local import *
Base = automap_base()
engine = create_engine(
    "postgres://%s:%s@%s/%s" %
    (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME))
Base.prepare(engine, reflect=True)

Persons = Base.classes.persons
Info = Base.classes.unsorted_info


def create_session():
    engine.dispose()
    Session = sessionmaker(bind=engine)
    return Session()
