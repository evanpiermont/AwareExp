

# from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_heroku import Heroku

app = Flask(__name__)

import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import create_engine

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kmwdsiybqohzkr:48c78dc82321c614a1f2058afdcf74987c7765b22a92be753f2a156d5299ad07@ec2-54-204-39-46.compute-1.amazonaws.com:5432/d40rkj7aib44id'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/awareExp'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:231207@localhost:5432/awareExp' #Felipe's local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#heroku = Heroku(app)
db = SQLAlchemy(app)

# deck is the set of all cards for all hands

class DeckSQL(db.Model):
    __tablename__ = "deck"

    id = Column(Integer, primary_key=True)
    color = Column(Integer)
    symbol = Column(Integer)
    number = Column(Integer)


# list of hands store them below.


class Hand(db.Model):
    __tablename__ = 'hand'

    id = Column(Integer, primary_key=True)
    hand_type = Column(Integer)

#for each hand, what are the consitutuent cards?

class HandByCard(db.Model):
    __tablename__ = 'hand_by_card'

    id = Column(Integer, primary_key=True)
    hand = Column(Integer, ForeignKey("hand.id"))
    card = Column(Integer, ForeignKey("deck.id"))


#returns all sets, stores which hand the sets are in, what are the three cards

class Sets(db.Model):
    __tablename__ = 'sets'
    id = Column(Integer, primary_key=True)
    hand = Column(Integer, ForeignKey("hand.id"))
    card1 = Column(Integer, ForeignKey("deck.id"))
    card2 = Column(Integer, ForeignKey("deck.id"))
    card3 = Column(Integer, ForeignKey("deck.id"))

#subjects, idcode is unique (hashed) idenifier for init and payment

class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    idCode = Column(String(100))
    hashed_id = Column(String(100))
    quizversion = Column(Integer, default=1)
    tryquiz = Column(Boolean, default=False)
    passquiz = Column(Boolean, default=False)
    age = Column(Integer)
    gender = Column(Integer)
    degree = Column(Integer)
    percent1 = Column(Integer)
    percent2 = Column(Integer)
    bet = Column(Integer)
    piecerate = Column(Integer, default=10)
    payment = Column(Integer, default=0)
    mobile = Column(Integer, default=0) #1 if mobile device, 0 if desktop

# who has which hand when?!?

class HandByRound(db.Model):
    __tablename__ = 'hand_by_round'
    id = Column(Integer, primary_key=True)
    subject = Column(Integer, ForeignKey("subject.id"))
    rnd = Column(Integer)
    hand = Column(Integer, ForeignKey("hand.id"))

# when did each round start for each subject?

class StartTimes(db.Model):
    __tablename__ = 'start_times'

    id = Column(Integer, primary_key=True)
    subject = Column(Integer, ForeignKey("subject.id"))
    rnd = Column(Integer)
    exptime = Column(DateTime)

#sets that hae been found

class Found(db.Model):
    __tablename__ = 'found'
    id = Column(Integer, primary_key=True)
    sets = Column(Integer, ForeignKey("sets.id"))
    subject = Column(Integer, ForeignKey("subject.id"))
    timefound = Column(DateTime)
    isset = Column(Boolean, default=False)
    novelset = Column(Boolean, default=False)
    hand = Column(Integer, ForeignKey("hand.id"))
    rnd = Column(Integer)


