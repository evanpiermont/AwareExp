

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import os
import datetime, time
from db_setup import Base, engine, DeckSQL, Hand, Subject, SType, Sets, Found
from setGame import Deck, getCards, isSetThreeCards
 
filePath = os.getcwd()
engine = create_engine('sqlite:///'+ filePath + '/set_am_turk.db')


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

foundarray = []

found = session.query(Found).all()
print found
# for s in found:
#     sets = session.query(Sets).filter(Sets.id == s.sets).one
#     card1 = session.query(DeckSQL).filter(DeckSQL.id == sets.card1)
#     card1 = session.query(DeckSQL).filter(DeckSQL.id == sets.card2)
#     card1 = session.query(DeckSQL).filter(DeckSQL.id == sets.card3)
#     # foundarray.append[[card1.color,card1.symbol,carcard2.color,card2.symbol,card2.number],[card3.color,card3.symbol,card3.number]]
#     foundarray.append['df']

# print foundarray



















