


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools, os

import db_setup

from db_setup import DeckSQL, Hand, HandByCard, Subject, Sets, Found, db
from setGame import Deck, getCards, isSetThreeCards, getNhands  
 


db.create_all()
    
session = db.session

setX = session.query(Sets).filter(Sets.card1 == 14, Sets.card2 == 37, Sets.card3 == 52, Sets.hand==20).one()



print(setX)

















