    

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools

import db_setup

from db_setup import DeckSQL, Hand, HandByCard, HandByRound, StartTimes, Subject, Sets, Found, db, app
from setGame import Deck, getCards, isSetThreeCards, getNhands  
 

# db.drop_all()
# db.create_all()

HandByRound.__table__.drop(db.engine, checkfirst=True)
StartTimes.__table__.drop(db.engine, checkfirst=True)
Found.__table__.drop(db.engine, checkfirst=True)
Selection.__table__.drop(db.engine, checkfirst=True)
Subject.__table__.drop(db.engine, checkfirst=True)


Subject.__table__.create(db.engine, checkfirst=True)
HandByRound.__table__.create(db.engine, checkfirst=True)
StartTimes.__table__.create(db.engine, checkfirst=True)
Found.__table__.create(db.engine, checkfirst=True)
Selection.__table__.create(db.engine, checkfirst=True)


session = db.session



print("tables are clear!")   


