from flask import Flask, request, redirect, url_for, render_template, jsonify

import os
import hashlib
import datetime, time, json
from datetime import datetime, timedelta
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer

# from flask_heroku import Heroku

from random import randint
import random

from db_setup import DeckSQL, Hand, Subject, Sets, Found, db, app
from setGame import Deck, getCards, isSetThreeCards, getNhands, threeProperties, getSubdeckNsets

import cgi
import collections, itertools

session = db.session

####
#####
######
####### __init__
######
#####
####

handsize = 12
rndtime = 200 #time in seconds
payment = 10
stype_max = 1 #number of s_types

super_small_decks = [[[1, 1, 2],[1, 2, 1],[3, 1, 0],[2, 1, 2],[0, 2, 1],[2, 2, 1],[2, 2, 3],[1, 2, 3],[1, 2, 0],[0, 1, 2],[2, 1, 1],[1, 2, 2]],
 [[3, 3, 0],[1, 1, 2],[0, 1, 2],[2, 1, 1],[3, 0, 0],[3, 3, 3],[0, 0, 3],[2, 1, 3],[3, 0, 2],[2, 1, 0],[0, 1, 1],[0, 0, 2]],
 [[3, 3, 0],[2, 3, 2],[3, 1, 0],[2, 1, 3],[2, 1, 2],[3, 0, 3],[1, 0, 0],[0, 0, 1],[3, 0, 2],[0, 0, 0],[1, 0, 2],[2, 1, 1]],
 [[1, 3, 1],[0, 1, 2],[0, 2, 3],[0, 3, 3],[1, 3, 0],[1, 0, 3],[0, 2, 0],[0, 3, 2],[0, 1, 3],[0, 0, 2],[0, 1, 0],[1, 0, 1]],
 [[3, 0, 1],[0, 2, 0],[3, 1, 3],[0, 0, 1],[1, 0, 3],[0, 2, 1],[0, 0, 3],[1, 0, 1],[3, 3, 3],[3, 0, 3],[1, 3, 1],[3, 3, 0]]]

small_decks = [[[0, 3, 0],[3, 0, 1],[1, 0, 3],[3, 0, 3],[3, 0, 2],[1, 0, 1],[0, 1, 2],[1, 1, 0],[1, 3, 2],[1, 2, 2],[0, 3, 3],[3, 3, 1]],
 [[1, 1, 1],[2, 3, 2],[0, 2, 2],[0, 2, 1],[0, 1, 3],[1, 2, 2],[1, 0, 2],[3, 1, 0],[0, 0, 2],[0, 1, 0],[1, 2, 3],[0, 3, 0]],
 [[1, 1, 1],[2, 0, 1],[1, 0, 0],[3, 0, 2],[1, 1, 3],[3, 1, 3],[0, 3, 1],[2, 3, 3],[3, 3, 2],[0, 2, 3],[1, 0, 2],[0, 3, 3]],
 [[2, 1, 2],[2, 2, 2],[3, 0, 3],[2, 2, 0],[1, 2, 0],[2, 1, 3],[1, 0, 1],[1, 0, 2],[3, 2, 1],[2, 0, 2],[0, 2, 3],[2, 0, 0]],
 [[1, 2, 3],[0, 0, 1],[0, 3, 3],[3, 3, 1],[0, 1, 1],[2, 0, 3],[3, 2, 3],[2, 3, 3],[3, 3, 2],[2, 0, 2],[0, 2, 0],[0, 2, 3]]]

large_decks = [[[0, 2, 1],[1, 3, 3],[1, 1, 3],[2, 2, 2],[1, 2, 2],[3, 2, 1],[2, 2, 1],[1, 0, 3],[3, 3, 0],[2, 1, 2],[2, 0, 1],[2, 3, 0]],
 [[1, 2, 2],[0, 1, 1],[2, 1, 3],[0, 0, 0],[1, 0, 2],[3, 3, 1],[2, 1, 1],[3, 0, 3],[2, 1, 2],[3, 1, 1],[0, 0, 3],[1, 2, 1]],
 [[3, 3, 3],[3, 2, 3],[2, 1, 3],[0, 1, 1],[3, 1, 1],[2, 3, 2],[1, 3, 0],[3, 2, 0],[2, 2, 0],[0, 1, 2],[3, 1, 0],[3, 0, 2]],
 [[2, 1, 2],[0, 3, 1],[3, 2, 3],[0, 1, 1],[3, 1, 2],[0, 3, 2],[1, 0, 2],[3, 0, 2],[0, 0, 1],[0, 2, 3],[2, 2, 3],[1, 2, 0]],
 [[3, 1, 2],[3, 0, 2],[1, 2, 3],[1, 2, 1],[0, 1, 0],[1, 1, 0],[1, 0, 1],[1, 3, 3],[2, 3, 1],[0, 3, 3],[3, 2, 1],[0, 0, 2]]]

super_large_decks = [[[1, 0, 1],[1, 0, 0],[2, 1, 0],[1, 3, 3],[3, 2, 2],[2, 2, 2],[3, 0, 2],[0, 2, 1],[0, 1, 3],[3, 3, 2],[0, 3, 3],[0, 0, 0]],
 [[2, 1, 3],[1, 0, 2],[2, 2, 2],[3, 0, 3],[0, 0, 1],[2, 1, 1],[0, 0, 0],[3, 3, 3],[0, 1, 0],[1, 2, 2],[3, 0, 0],[2, 3, 1]],
 [[2, 0, 0],[0, 2, 2],[1, 0, 0],[2, 2, 2],[0, 3, 1],[2, 0, 1],[3, 0, 0],[1, 2, 0],[1, 0, 1],[1, 2, 2],[3, 1, 3],[0, 1, 3]],
 [[0, 1, 1],[2, 0, 2],[1, 3, 0],[2, 2, 2],[1, 2, 2],[0, 3, 2],[3, 2, 2],[2, 3, 0],[0, 0, 1],[1, 0, 3],[1, 1, 0],[1, 3, 3]],
 [[2, 3, 0],[3, 0, 2],[1, 0, 1],[3, 0, 0],[1, 2, 2],[1, 2, 1],[3, 0, 3],[0, 3, 1],[3, 1, 1],[2, 1, 0],[0, 3, 0],[0, 0, 3]]]

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
        #return Quiz(subject_id) 


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
            return render_template('instructions.html', subject_id = subject_id)


@app.route('/compquiz/<subject_id>', methods=['POST', 'GET'])
def Quiz(subject_id):

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()


    if j.tryquiz:

        return render_template('login.html', text='You already failed the quiz.', v=True)

    else:
        return render_template('quiz.html', subject_id = subject_id)

@app.route('/quizval', methods=['POST'])
def QuizVal():

    subject_id=str(request.form['subject_id'])

    a1=int(request.form['set1'])
    a2=int(request.form['set2'])
    a3=int(request.form['set3'])
    a4=int(request.form['set4'])
    a5=int(request.form['set5'])

    correct = a1 + a2 + a3 + a4 + a5

    if correct > 3:

        j = session.query(Subject).filter(Subject.idCode == subject_id).one()
        j.tryquiz = True
        j.passquiz = True
        session.add(j)
        session.commit()

        return CreateSets(subject_id)

    else:

        j = session.query(Subject).filter(Subject.idCode == subject_id).one()
        j.tryquiz = True
        j.passquiz = False
        session.add(j)
        session.commit()

        return render_template('login.html', text='You failed the quiz.', v=True)






    

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

                j.exptime = datetime.now() + timedelta(seconds=+rndtime)
                session.add(j)
                session.commit()


            if diff_seconds < 0:
                
                return render_template('login.html', text='Sorry, you have already played', v=True)

            elif not j.passquiz:

                return render_template('login.html', text='Sorry, you have failed the quiz', v=True)

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
    
                return render_template('set.html', subject_id = subject_id, handarray=handarray, handIDarray=handIDarray, foundarray=foundarray, foundIDarray=foundIDarray, diff_seconds=diff_seconds, found_sets_num=found_sets_num)


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
####### Survey PAGE
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

             

@app.route('/viz', methods=['POST','get'])
# def Viz():
# 
#     handIDarray = []
#     for i in range(12):
#         handIDarray.append(i)
# 
# 
#     handarray=getNhands(threeProperties, 12, 1)[0]
# 
#     total = 0
# 
#     C = list(itertools.combinations(handarray, 3))
#     for i in C:
#         if isSetThreeCards(i):
#             total += 1
# 
#     return render_template('set.html', subject_id=total, handarray=handarray, handIDarray=handIDarray, foundarray=[], foundIDarray=[], diff_seconds=1000, found_sets_num=0)

def Viz():

    handIDarray = []
    for i in range(12):
        handIDarray.append(i)
        
    # randomly pick among list with few sets or list of lots of sets
    if random.random() > 0.5:
        handarray = random.choice(super_small_decks) #manually computed from setGame.py
    else:
        handarray = random.choice(super_large_decks) #manually computed from setGame.py

    total = 0
    C = list(itertools.combinations(handarray, 3))
    for i in C:
        if isSetThreeCards(i):
            total += 1

    return render_template('set.html', subject_id=total, handarray=handarray, handIDarray=handIDarray, foundarray=[], foundIDarray=[], diff_seconds=1000, found_sets_num=0)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

 