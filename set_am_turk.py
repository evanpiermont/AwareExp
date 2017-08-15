from flask import Flask, request, redirect, url_for, render_template, jsonify
app = Flask(__name__)

import os
import hashlib
import datetime, time, json
from datetime import datetime, timedelta
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer

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
rndtime = 120 #time in seconds
payment = 10
stype_max = 2 #number of s_types


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
####### User information page
######
#####
####

@app.route('/user_manual', methods=['POST', 'GET'])
def Manual():

    subject_id=request.form['subject_id']

    return redirect(url_for('newUser', workerID=subject_id), code=302)


@app.route('/user/', methods=['POST', 'GET'])
def newUser():

    subject_id = request.args.get('workerID')

    if not subject_id or len(subject_id) < 5:

        return render_template('login.html', text='Enter a valid subject number.', v=True)

    else:
        sub = session.query(Subject).all()
        subjectnames = []
        for i in sub:
               subjectnames.append(i.idCode)
    
            #get list of valid subject names, next we test the input name to
            #sure the imput is valid
    
        if subject_id not in subjectnames:

            hashed_id = hashlib.sha1(subject_id.encode("UTF-8")).hexdigest()[:8]
            s_type = randint(1,stype_max)
        
            subject = Subject(
                idCode= subject_id,
                hashed_id = hashed_id,
                s_type = s_type)
            session.add(subject)
            session.commit()
    
        return Instructions(subject_id) 


@app.route('/instructions/<subject_id>', methods=['POST', 'GET'])
def Instructions(subject_id):

        sub = session.query(Subject).all()
        subjectnames = []
        for i in sub:
           subjectnames.append(i.idCode)

        #get list of valid subject names, next we test the input name to
        #sure the imput is valid

        if subject_id not in subjectnames:

            return render_template('login.html', text='Enter a valid subject number.', v=True)

        else:
            return render_template('instructions.html', subject_id = subject_id, handsize=handsize, rndtime=rndtime)


####
#####
######
####### Create Sets Page
######
#####
####

@app.route('/createsets/<subject_id>', methods=['POST', 'GET'])
def CreateSets(subject_id):

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
####### Surevey PAGE
######
#####
####

@app.route('/survey', methods=['POST'])
def Survey():

    subject_id=str(request.form['subject_id'])

    return render_template('survey.html', subject_id=subject_id)



####
#####
######
####### END PAGE
######
#####
####

@app.route('/end', methods=['POST'])
def End():

    subject_id=str(request.form['subject_id'])

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()

    j.gender = request.form['gender']
    j.race = request.form['race']
    j.degree = request.form['degree']
    j.percent = request.form['percent']
    j.half = request.form['half']
    j.bet = request.form['bet']
    j.star = request.form['star']

    session.add(j)
    session.commit()

    found_num = session.query(Found).filter(Found.subject == j.id).count()

    hashed_id = j.hashed_id

    paycode = subject_id + ".." + str(found_num)
    return render_template('login.html', text="Thank you; your paycode is: " + hashed_id, v=False)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



