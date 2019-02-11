
    

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools

import db_setup

from db_setup import DeckSQL, Hand, HandByCard, HandByRound, Subject, Sets, Found, db
from setGame import Deck, getCards, isSetThreeCards, getNhands  
 


session = db.session

subject_id = 'ssdddd'
i = 1
j = session.query(Subject).all()

for k in j:
    print(k.idCode, k.mobile)



















