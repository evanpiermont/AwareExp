

# from flask_sqlalchemy import SQLAlchemy

import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import create_engine

Base = declarative_base()

# deck is the set of all cards for all hands

class DeckSQL(Base):
    __tablename__ = "deck"

    id = Column(Integer, primary_key=True)
    color = Column(Integer)
    symbol = Column(Integer)
    number = Column(Integer)


# pick some hands from the deck, store them below. every card/type pair


class Hand(Base):
    __tablename__ = 'hand'

    id = Column(Integer, primary_key=True)
    card = Column(Integer, ForeignKey("deck.id"))
    color = Column(Integer)
    symbol = Column(Integer)
    number = Column(Integer)
    s_type = Column(Integer, ForeignKey("s_type.id"))


#returns all sets, stores which hand the sets are in, what are the three cards

class Sets(Base):
    __tablename__ = 'sets' 
    id = Column(Integer, primary_key=True)
    s_type = Column(Integer, ForeignKey("hand.id"))
    card1 = Column(Integer, ForeignKey("deck.id"))
    card2 = Column(Integer, ForeignKey("deck.id"))
    card3 = Column(Integer, ForeignKey("deck.id"))

#subjects, idcode is unique (hashed) idenifier for init and payment

class Subject(Base):
    __tablename__ = 'subject' 
    id = Column(Integer, primary_key=True)
    idCode = Column(String(100))
    hashed_id = Column(String(100))
    s_type = Column(Integer, ForeignKey("s_type.id"))
    exptime = Column(DateTime)
    gender = Column(Integer)
    race = Column(Integer)
    degree = Column(Integer)
    percent = Column(Integer)
    half = Column(Integer)
    bet = Column(Integer)
    star = Column(Integer)

# types are non-unique by subject, encode the hand, lazy way of getting around problems with encoding

class SType(Base):
    __tablename__ = 's_type' 
    id = Column(Integer, primary_key=True)


#sets that hae been found

class Found(Base):
    __tablename__ = 'found' 
    id = Column(Integer, primary_key=True)
    sets = Column(Integer, ForeignKey("sets.id"))
    subject = Column(Integer, ForeignKey("subject.id"))



filePath = os.getcwd()
engine = create_engine('postgres://kmwdsiybqohzkr:48c78dc82321c614a1f2058afdcf74987c7765b22a92be753f2a156d5299ad07@ec2-54-204-39-46.compute-1.amazonaws.com:5432/d40rkj7aib44id')


Base.metadata.create_all(engine)

