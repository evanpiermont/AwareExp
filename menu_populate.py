    

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools, os

import db_setup

from db_setup import DeckSQL, Hand, Subject, Sets, Found, db
from setGame import Deck, getCards, isSetThreeCards
 


db.create_all()
    
session = db.session


currentdeck = Deck({'number':[0,1,2,3],'symbol':[0,1,2,3], 'color':[0,1,2,3]})

allCards = getCards(currentdeck)

def cardFromIndex(index): #need to subtract 1 becuase SQL starts counting at 1
    return allCards[index-1]

for i in allCards:
    deck = DeckSQL(
    color = i[0],
    symbol = i[1],
    number = i[2])

    session.add(deck)
    session.commit()


s_type1 = 1

for i in [1,7,34,42,41,51,55,17,9]:
    q = session.query(DeckSQL).filter(DeckSQL.id == i).one()
    hand = Hand(
        card = i,
        color = q.color,
        symbol = q.symbol,
        number = q.number,
        s_type = s_type1,
        )
    session.add(hand)
    session.commit()

k = session.query(Hand).filter(Hand.s_type == 1).all()

handarrayindex = []

for i in k:
    handarrayindex.append(i.card)

C = list(itertools.combinations(handarrayindex, 3))
for i in C:
    cards = list(map(cardFromIndex, i))
    if isSetThreeCards(cards):
        j = list(i)
        j.sort()
        sets = Sets(
            s_type = s_type1,
            card1 = j[0],
            card2 = j[1],
            card3 = j[2])   
        session.add(sets)
        session.commit() 


#### do this more efficently in the future

s_type1 = 2

for i in [27,26,25,24,23,22,21,20,19]:
    q = session.query(DeckSQL).filter(DeckSQL.id == i).one()
    hand = Hand(
        card = i,
        color = q.color,
        symbol = q.symbol,
        number = q.number,
        s_type = s_type1,
        )
    session.add(hand)
    session.commit()

k = session.query(Hand).filter(Hand.s_type == 2).all()

handarrayindex = []

for i in k:
    handarrayindex.append(i.card)

C = list(itertools.combinations(handarrayindex, 3))
for i in C:
    cards = list(map(cardFromIndex, i))
    if isSetThreeCards(cards):
        j = list(i)
        j.sort()
        sets = Sets(
            s_type = s_type1,
            card1 = j[0],
            card2 = j[1],
            card3 = j[2])   
        session.add(sets)
        session.commit() 






print("added stuff!")   


