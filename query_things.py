

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import os
import datetime, time
from db_setup import Base, engine, Deck, Hand, Subject, Sets, FoundSets
 
 
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


q = session.query(Subject).all()

for i in q:
	h = session.query(Hand).filter(Hand.id == Subject.hand).one()
	h.join(Deck)
	print handarray


















