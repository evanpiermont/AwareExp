

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import os

import db_setup

from db_setup import Base, engine, Deck, Hand, Subject, Sets, FoundSets
 
filePath = os.getcwd()
os.remove(filePath + '/set_am_turk.db')
db_setup.Base.metadata.create_all(engine)


#engine = create_engine('sqlite:////Users/evanpiermont/Desktop/scrabble/restaurantmenu.db')
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

for i in range(0,3):
    for j in range(0,3):
        for k in range(0,3):
            deck = Deck(
            color = i,
            symbol = j,
            number = k)

            session.add(deck)
            session.commit()

hand = Hand(
    card1 = 1,
    card2 = 2,
    card3 = 3,
    card4 = 4,
    card5 = 5,
    card6 = 6,
    card7 = 7,
    card8 = 8,
    card9 = 9)

session.add(hand)
session.commit()

subject = Subject(
    idCode = 1,
    hand = 1)

session.add(subject)
session.commit()


print "added stuff!"


