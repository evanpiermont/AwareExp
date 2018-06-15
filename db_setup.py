

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


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kmwdsiybqohzkr:48c78dc82321c614a1f2058afdcf74987c7765b22a92be753f2a156d5299ad07@ec2-54-204-39-46.compute-1.amazonaws.com:5432/d40rkj7aib44id'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/awareExp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# deck is the set of all cards for all hands

class DeckSQL(db.Model):
    __tablename__ = "deck"

    id = Column(Integer, primary_key=True)
    color = Column(Integer)
    symbol = Column(Integer)
    number = Column(Integer)


# pick some hands from the deck, store them below. every card/type pair


class Hand(db.Model):
    __tablename__ = 'hand'

    id = Column(Integer, primary_key=True)
    card = Column(Integer, ForeignKey("deck.id"))
    color = Column(Integer)
    symbol = Column(Integer)
    number = Column(Integer)
    #s_type = Column(Integer, ForeignKey("s_type.id"))
    s_type = Column(Integer)


#returns all sets, stores which hand the sets are in, what are the three cards

class Sets(db.Model):
    __tablename__ = 'sets' 
    id = Column(Integer, primary_key=True)
    s_type = Column(Integer, ForeignKey("hand.id"))
    card1 = Column(Integer, ForeignKey("deck.id"))
    card2 = Column(Integer, ForeignKey("deck.id"))
    card3 = Column(Integer, ForeignKey("deck.id"))

#subjects, idcode is unique (hashed) idenifier for init and payment

class Subject(db.Model):
    __tablename__ = 'subject' 
    id = Column(Integer, primary_key=True)
    idCode = Column(String(100))
    hashed_id = Column(String(100))
    # s_type = Column(Integer, ForeignKey("s_type.id"))
    s_type = Column(Integer)
    tryquiz = Column(Boolean, default=False)
    passquiz = Column(Boolean, default=False)
    exptime = Column(DateTime)
    gender = Column(Integer)
    race = Column(Integer)
    degree = Column(Integer)
    percent = Column(Integer)
    half = Column(Integer)
    bet = Column(Integer)
    star = Column(Integer)

# types are non-unique by subject, encode the hand, lazy way of getting around problems with encoding

# class SType(db.Model):
#     __tablename__ = 's_type' 
#     id = Column(Integer, primary_key=True)


#sets that hae been found

class Found(db.Model):
    __tablename__ = 'found' 
    id = Column(Integer, primary_key=True)
    sets = Column(Integer, ForeignKey("sets.id"))
    subject = Column(Integer, ForeignKey("subject.id"))




