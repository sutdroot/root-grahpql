from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import json

# engine = create_engine('postgresql://postgres:password@localhost:5432/data')
with open('config.json') as f:
    db_url = json.load(f)['SQLALCHEMY_DATABASE_URI']

engine = create_engine(db_url)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import Feedback
    Base.metadata.create_all(bind=engine)

    db_session.commit()
