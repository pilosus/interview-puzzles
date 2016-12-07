# source:
# http://stackoverflow.com/a/22357235/4241180

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(u'sqlite:///:memory:', echo=True)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# User can be either a receiver, or sender in the dialogue
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Dialogue(Base):
    __tablename__ = 'dialogues'
    id = Column(Integer, primary_key=True)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver = relationship("User", foreign_keys=[receiver_id])
    sender = relationship("User", foreign_keys=[sender_id])

Base.metadata.create_all(engine)

# filtering with logical OR
# http://stackoverflow.com/q/7942547/4241180

# session.query(Dialogue).filter((Dialogue.sender==u1) | (Dialogue.receiver==u1)).all()