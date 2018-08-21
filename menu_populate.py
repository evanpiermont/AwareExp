    

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import itertools

import db_setup

from db_setup import DeckSQL, Hand, HandByCard, Subject, Sets, Found, db
from setGame import Deck, getCards, isSetThreeCards, getNhands  
 

db.drop_all()
db.create_all()
    
session = db.session


currentdeck = Deck({'number':[0,1,2,3],'symbol':[0,1,2,3], 'color':[0,1,2,3]})

#encoded into dict: 0 = super_small_decks, 1 = small, 2 = large, 3 = super large

allHands = {
0:[[[1, 1, 2],[1, 2, 1],[3, 1, 0],[2, 1, 2],[0, 2, 1],[2, 2, 1],[2, 2, 3],[1, 2, 3],[1, 2, 0],[0, 1, 2],[2, 1, 1],[1, 2, 2]],
 [[3, 3, 0],[1, 1, 2],[0, 1, 2],[2, 1, 1],[3, 0, 0],[3, 3, 3],[0, 0, 3],[2, 1, 3],[3, 0, 2],[2, 1, 0],[0, 1, 1],[0, 0, 2]],
 [[3, 3, 0],[2, 3, 2],[3, 1, 0],[2, 1, 3],[2, 1, 2],[3, 0, 3],[1, 0, 0],[0, 0, 1],[3, 0, 2],[0, 0, 0],[1, 0, 2],[2, 1, 1]],
 [[1, 3, 1],[0, 1, 2],[0, 2, 3],[0, 3, 3],[1, 3, 0],[1, 0, 3],[0, 2, 0],[0, 3, 2],[0, 1, 3],[0, 0, 2],[0, 1, 0],[1, 0, 1]],
 [[3, 0, 1],[0, 2, 0],[3, 1, 3],[0, 0, 1],[1, 0, 3],[0, 2, 1],[0, 0, 3],[1, 0, 1],[3, 3, 3],[3, 0, 3],[1, 3, 1],[3, 3, 0]]],
1:[[[0, 3, 0],[3, 0, 1],[1, 0, 3],[3, 0, 3],[3, 0, 2],[1, 0, 1],[0, 1, 2],[1, 1, 0],[1, 3, 2],[1, 2, 2],[0, 3, 3],[3, 3, 1]],
 [[1, 1, 1],[2, 3, 2],[0, 2, 2],[0, 2, 1],[0, 1, 3],[1, 2, 2],[1, 0, 2],[3, 1, 0],[0, 0, 2],[0, 1, 0],[1, 2, 3],[0, 3, 0]],
 [[1, 1, 1],[2, 0, 1],[1, 0, 0],[3, 0, 2],[1, 1, 3],[3, 1, 3],[0, 3, 1],[2, 3, 3],[3, 3, 2],[0, 2, 3],[1, 0, 2],[0, 3, 3]],
 [[2, 1, 2],[2, 2, 2],[3, 0, 3],[2, 2, 0],[1, 2, 0],[2, 1, 3],[1, 0, 1],[1, 0, 2],[3, 2, 1],[2, 0, 2],[0, 2, 3],[2, 0, 0]],
 [[1, 2, 3],[0, 0, 1],[0, 3, 3],[3, 3, 1],[0, 1, 1],[2, 0, 3],[3, 2, 3],[2, 3, 3],[3, 3, 2],[2, 0, 2],[0, 2, 0],[0, 2, 3]]],
2:[[[0, 2, 1],[1, 3, 3],[1, 1, 3],[2, 2, 2],[1, 2, 2],[3, 2, 1],[2, 2, 1],[1, 0, 3],[3, 3, 0],[2, 1, 2],[2, 0, 1],[2, 3, 0]],
 [[1, 2, 2],[0, 1, 1],[2, 1, 3],[0, 0, 0],[1, 0, 2],[3, 3, 1],[2, 1, 1],[3, 0, 3],[2, 1, 2],[3, 1, 1],[0, 0, 3],[1, 2, 1]],
 [[3, 3, 3],[3, 2, 3],[2, 1, 3],[0, 1, 1],[3, 1, 1],[2, 3, 2],[1, 3, 0],[3, 2, 0],[2, 2, 0],[0, 1, 2],[3, 1, 0],[3, 0, 2]],
 [[2, 1, 2],[0, 3, 1],[3, 2, 3],[0, 1, 1],[3, 1, 2],[0, 3, 2],[1, 0, 2],[3, 0, 2],[0, 0, 1],[0, 2, 3],[2, 2, 3],[1, 2, 0]],
 [[3, 1, 2],[3, 0, 2],[1, 2, 3],[1, 2, 1],[0, 1, 0],[1, 1, 0],[1, 0, 1],[1, 3, 3],[2, 3, 1],[0, 3, 3],[3, 2, 1],[0, 0, 2]]],
3:[[[1, 0, 1],[1, 0, 0],[2, 1, 0],[1, 3, 3],[3, 2, 2],[2, 2, 2],[3, 0, 2],[0, 2, 1],[0, 1, 3],[3, 3, 2],[0, 3, 3],[0, 0, 0]],
 [[2, 1, 3],[1, 0, 2],[2, 2, 2],[3, 0, 3],[0, 0, 1],[2, 1, 1],[0, 0, 0],[3, 3, 3],[0, 1, 0],[1, 2, 2],[3, 0, 0],[2, 3, 1]],
 [[2, 0, 0],[0, 2, 2],[1, 0, 0],[2, 2, 2],[0, 3, 1],[2, 0, 1],[3, 0, 0],[1, 2, 0],[1, 0, 1],[1, 2, 2],[3, 1, 3],[0, 1, 3]],
 [[0, 1, 1],[2, 0, 2],[1, 3, 0],[2, 2, 2],[1, 2, 2],[0, 3, 2],[3, 2, 2],[2, 3, 0],[0, 0, 1],[1, 0, 3],[1, 1, 0],[1, 3, 3]],
 [[2, 3, 0],[3, 0, 2],[1, 0, 1],[3, 0, 0],[1, 2, 2],[1, 2, 1],[3, 0, 3],[0, 3, 1],[3, 1, 1],[2, 1, 0],[0, 3, 0],[0, 0, 3]]]
}

allCards = getCards(currentdeck)

def cardFromIndex(index): #need to subtract 1 becuase SQL starts counting at 1
    return allCards[index-1]

for i in allCards:
    #if session.query(DeckSQL).filter(DeckSQL.color == i[0], DeckSQL.symbol == i[1], DeckSQL.number == i[2]) == None:
    
        deck = DeckSQL(
        color = i[0],
        symbol = i[1],
        number = i[2])
    
        session.add(deck)
        session.commit()
    



for handtype in allHands:

    for hand in allHands[handtype]:

        new_hand = Hand(
            hand_type = handtype)
        session.add(new_hand)
        session.commit()

        for card in hand:
            q = session.query(DeckSQL).filter(DeckSQL.color == card[0], DeckSQL.symbol == card[1], DeckSQL.number == card[2]).one()
            last_hand = session.query(Hand).order_by(Hand.id.desc()).first()
            new_hand_by_card = HandByCard(
                card = q.id,
                hand = last_hand.id)
            session.add(new_hand_by_card)
            session.commit()



hands = session.query(Hand).all()

for hand in hands:
    handarrayindex = []
    cards = session.query(HandByCard).filter(HandByCard.hand == hand.id).all()
    for card in cards:
        cardid = session.query(DeckSQL).filter(DeckSQL.id == card.card).one()
        handarrayindex.append(cardid.id)
    #print(handarrayindex)

    C = list(itertools.combinations(handarrayindex, 3))
    for i in C:
        cards = list(map(cardFromIndex, i))
        if isSetThreeCards(cards):
            j = list(i)
            j.sort()
            sets = Sets(
                hand = hand.id,
                card1 = j[0],
                card2 = j[1],
                card3 = j[2])   
            session.add(sets)
    session.commit() 


# #### do this more efficently in the future

# s_type1 = 2

# for i in [27,26,25,24,23,22,21,20,19,11,2,3]:
#     q = session.query(DeckSQL).filter(DeckSQL.id == i).one()
#     hand = Hand(
#         card = i,
#         color = q.color,
#         symbol = q.symbol,
#         number = q.number,
#         s_type = s_type1,
#         )
#     session.add(hand)
#     session.commit()

# k = session.query(Hand).filter(Hand.s_type == 2).all()

# handarrayindex = []

# for i in k:
#     handarrayindex.append(i.card)

# C = list(itertools.combinations(handarrayindex, 3))
# for i in C:
#     cards = list(map(cardFromIndex, i))
#     if isSetThreeCards(cards):
#         j = list(i)
#         j.sort()
#         sets = Sets(
#             s_type = s_type1,
#             card1 = j[0],
#             card2 = j[1],
#             card3 = j[2])   
#         session.add(sets)
#         session.commit() 






print("added stuff!")   


