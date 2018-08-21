


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools, os

import db_setup

from db_setup import DeckSQL, Hand, HandByCard, Subject, Sets, Found, db
from setGame import Deck, getCards, isSetThreeCards, getNhands  
 


session = db.session

setX = session.query(Sets).all()

for k in setX:
    print(k.hand)



















