from flask import Flask, request, redirect, url_for, render_template, jsonify
app = Flask(__name__)

import os
import datetime, time, json
from datetime import datetime, timedelta
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
####### __init__
######
#####
####

handsize = 9
rndtime = 35 #time in seconds


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
    return render_template('login.html', v="Please enter a subject number.")

####
#####
######
####### Create Sets Page
######
#####
####

@app.route('/createsets', methods=['POST', 'GET'])
def CreateSets():

        subject_id=int(request.form['subject_id'])

        sub = session.query(Subject).all()
        subjectnames = []
        for i in sub:
           subjectnames.append(i.idCode)

        #get list of valid subject names, next we test the input name to
        #sure the imput is valid

        if subject_id not in subjectnames:

            return render_template('login.html', text='Enter a valid subject number.', v=True)

        else:

            j = session.query(Subject).filter(Subject.idCode == subject_id).one()

            diff_seconds = rndtime

            if j.exptime:

                diff = j.exptime - datetime.now()
                diff = diff - timedelta(microseconds=diff.microseconds)
                diff_seconds= diff.total_seconds()

            else:

                time = datetime.now()
                exptime = time + timedelta(seconds=+rndtime)
                j.exptime = exptime
                session.add(j)
                session.commit


            if diff_seconds < 0:
                
                return render_template('login.html', text='Sorry, you have already played', v=True)

            else:

                k = session.query(Hand).filter(Hand.s_type == j.s_type).limit(handsize).all()
    
                handarray = []
                handIDarray = []
    
                for i in k:
                    handarray.append([i.color,i.symbol,i.number])
                    handIDarray.append(i.card)
    
                foundarray = []
                foundIDarray = []
    
                found = session.query(Found).filter(Found.subject == j.id).all()
    
                for s in found:
                    setX = session.query(Sets).filter(Sets.id == s.sets).one()
                    card1 = session.query(DeckSQL).filter(DeckSQL.id == setX.card1).one()
                    card2 = session.query(DeckSQL).filter(DeckSQL.id == setX.card2).one()
                    card3 = session.query(DeckSQL).filter(DeckSQL.id == setX.card3).one()
                    foundarray.append([[card1.color,card1.symbol,card1.number],[card2.color,card2.symbol,card2.number   ],[card3.color,card3.symbol,card3.number]])
                    foundIDarray.append([setX.card1,setX.card2,setX.card3])
    
                found_sets_num = len(foundIDarray)
    
                return render_template('set.html', subject_id = subject_id, handarray=handarray, handIDarray=   handIDarray, foundarray=foundarray, foundIDarray=foundIDarray, diff_seconds=diff_seconds, found_sets_num=found_sets_num)


@app.route('/_add_set', methods=['POST'])
def AddSetJSON():

    cardsX=request.form['cardsX']
    subject_id=request.form['subject_id']
    cardsX=json.loads(cardsX)

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()

    setX = session.query(Sets).filter(Sets.card1 == cardsX[0], Sets.card2 == cardsX[1], Sets.card3 == cardsX[2]).one()

    newset = Found(
        sets = setX.id,
        subject = j.id)
    session.add(newset)
    session.commit()
 
    return jsonify(foundarray = setX.id)


####
#####
######
####### LOGIN PAGE
######
#####
####

@app.route('/end', methods=['POST'])
def End():

    found_num=str(request.form['found_num'])
    subject_id=str(request.form['subject_id'])

    paycode = subject_id + ".." + found_num
    return render_template('login.html', text="Thank you; your paycode is: " + paycode, v=False)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



