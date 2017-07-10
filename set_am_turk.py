from flask import Flask, request, redirect, url_for, render_template, jsonify
app = Flask(__name__)

import os
import datetime, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from random import randint

from db_setup import Base, DeckSQL, Hand, Subject, SType, Sets, Found

import cgi
import collections


filePath = os.getcwd()
engine = create_engine('sqlite:///'+ filePath + '/set_am_turk.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

####
#####
######
####### LOGIN PAGE
######
#####
####

@app.route('/')
@app.route('/login')
def Login():
    return render_template('login.html', v=True)

####
#####
######
####### Create Sets Page
######
#####
####

@app.route('/createsets', methods=['POST', 'GET'])
def CreateSets():

 
        subject_id=request.form['subject_id']

        sub = session.query(Subject).all()
        subjectnames = []
        for i in sub:
           subjectnames.append(i.idCode)

        #get list of valid subject names, next we test the input name to
        #sure the imput is valid

        if subject_id not in subjectnames:

            j = session.query(Subject).filter(Subject.idCode == subject_id).one() 

            k = session.query(Hand).filter(Hand.s_type == j.s_type).all()

            handarray = []

            for i in k:
                handarray.append([i.color,i.symbol,i.number])

            foundarray = []

            found = session.query(Found).filter(Found.subject == j.id).all()

            for s in found:
                setX = session.query(Sets).filter(Sets.id == s.sets).one()
                card1 = session.query(DeckSQL).filter(DeckSQL.id == setX.card1).one()
                card2 = session.query(DeckSQL).filter(DeckSQL.id == setX.card2).one()
                card3 = session.query(DeckSQL).filter(DeckSQL.id == setX.card3).one()
                foundarray.append([[card1.color,card1.symbol,card1.number],[card2.color,card2.symbol,card2.number],[card3.color,card3.symbol,card3.number]])



            return render_template('set.html', subject_id = subject_id, handarray=handarray, foundarray=foundarray)

        else:
            return render_template('login.html', v=False)




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



