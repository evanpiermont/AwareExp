
    

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools

import db_setup

from db_setup import DeckSQL, Hand, HandByCard, HandByRound, Subject, Sets, Found, db
from setGame import Deck, getCards, isSetThreeCards, getNhands  
 


session = db.session

subject_id = 'sdvfbgnbefsd'
i = 1
j = session.query(Subject).filter(Subject.idCode == subject_id).one()
hand = session.query(HandByRound).filter(HandByRound.rnd == i, HandByRound.subject==j.id).one()
#next how many total
sets = session.query(Sets).filter(Sets.hand == hand.hand).all()

for k in sets:
    print(k.id)



















