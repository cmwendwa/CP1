from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Persons(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    person_id = Column(String(120), unique=True)
    person_type = Column(String(30))
    email = Column(String(120))
    name = Column(String(50))
    wants_accomodation = Column(String(12))
    allocated_living = Column(String(120))
    allocated_office = Column(String(120))

    def __repr__(self):
        return "<Person(person_name='%s')>" % self.name


class Rooms(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    room_type = Column(String(10))


    def __repr__(self):
        return "<Room(room_name='%s')>" % self.name


class DbManager(object):
  """
  creates database connection object
  
  """
  def __init__(self, db_name=None):
    if db_name:
        self.name = db_name + '.sqlite'
    else:
        self.name = 'amity_db.sqlite'
    self.engine = create_engine('sqlite:///' + self.name)
    self.session = sessionmaker()
    self.session.configure(bind=self.engine)
    Base.metadata.create_all(self.engine)
