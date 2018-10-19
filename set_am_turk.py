from __future__ import division
from flask import Flask, request, redirect, url_for, render_template, jsonify, Markup

import os
import hashlib
import datetime, time, json
from datetime import datetime, timedelta
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer

# from flask_heroku import Heroku

from random import randint
import random

from db_setup import DeckSQL, Hand, HandByCard, HandByRound, StartTimes, Subject, Sets, Found, db, app
#from setGame import Deck, getCards, isSetThreeCards, getNhands, threeProperties, getSubdeckNsets

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

handsize = 12 #number of cards per hand
rndtime = 10 #time in seconds
piecerate = [10,25] #payment in cents per correct anwser
fixed_payment = 25 #fixed payment in cents
belief_payment = 25 #elictation of beliefs bonus payment in cents
rounds = 2 #number of rounds.
time_penalty = 500 #length of penalty in MILIseconds
quizversions = [[1,0,0,1,0],[0,0,1,1,1],[1,1,0,0,1],[0,1,1,1,0]] #list of correct answers for each verison of the quiz 

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


        return render_template('login.html', text='Enter a subject number.', action='/user_manual', input=True, v=True)


####
#####
######
####### User information page
######
#####
####

### This route is the main landing page, it allows us to enter a username manually. It will accept
### any 6 or more charecter string as a user name (this is validated later, via the /user route)
### redirects to the /user with a formated URL

@app.route('/user_manual', methods=['POST', 'GET'])
def Manual():

    subject_id=request.form['subject_id']

    return redirect(url_for('newUser', workerId=subject_id), code=302)


### This is the route from M-TURK. takes the worker ID from the URL under workerID
### enters the subject if it does not exist in the data base.

@app.route('/user/', methods=['POST', 'GET'])
def newUser():

    subject_id = request.args.get('workerId')

    if len(subject_id) < 5:

        ### we resuse the login page as a prompt for payment, so v=true allows username entry.

        return render_template('login.html', text='Enter a valid subject number.', action='/user_manual', input=True, v=True)

    elif session.query(Subject).filter(Subject.idCode == subject_id).count() == 0:

        hashed_id = hashlib.sha1(subject_id.encode("UTF-8")).hexdigest()[:8]
        q = random.randint(0,len(quizversions)-1) #choose quiz version
        p = random.choice(piecerate)
                
        subject = Subject(
            idCode= subject_id,
            hashed_id = hashed_id,
            quizversion = q,
            piecerate = p,
            payment = fixed_payment)    
        session.add(subject)
        session.commit()
        hands = session.query(Hand).all() #all possible hands
        random.seed(datetime.now())
        handarray = random.sample(hands, rounds) #random sample, 1 for each round
        j = session.query(Subject).filter(Subject.idCode == subject_id).one()
        
        for rnd in range(rounds):
            new_hand_by_round = HandByRound(
                subject = j.id,
                rnd = rnd,
                hand = handarray[rnd].id)
            session.add(new_hand_by_round)
            session.commit()

        return render_template('instructions.html', subject_id = subject_id, piecerate=str(round(p/100, 2)), rounds=str(rounds), fixed_payment=str(round(fixed_payment/100, 2)))
        #return Quiz(subject_id) 
    else:
            return render_template('login.html', text='You have already played.', action='/user_manual', v=False)




### just routes the guy to the quiz. we could obviously totally get around this by formatting URLS
### and just making the redirect from the instructions directly. but why not. 

@app.route('/compquiz/<subject_id>', methods=['POST', 'GET'])
def Quiz(subject_id):

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()


    if j.tryquiz:

        return render_template('login.html', text='You have already failed the quiz.', input=False, v=True)

    else:
        q = j.quizversion
        return render_template('quiz.html', subject_id = subject_id, q=q)

### now we need to make sure they passed the quiz. 

@app.route('/quizval', methods=['POST'])
def QuizVal():

    subject_id=str(request.form['subject_id'])
    j = session.query(Subject).filter(Subject.idCode == subject_id).one()


    if j.tryquiz:
        return render_template('login.html', text='You have already failed the quiz.', input=False, v=True)

    quiz_ans=[int(request.form['set1']),int(request.form['set2']),int(request.form['set3']),int(request.form['set4']),int(request.form['set5'])]
    correct = quizversions[j.quizversion]
 
    print([(x+y)%2 for x, y in zip(quiz_ans, correct)])
    if [(x+y)%2 for x, y in zip(quiz_ans, correct)] == [0,0,0,0,0]:

        j.tryquiz = True
        j.passquiz = True
        session.add(j)
        session.commit()

        return WaitNext(subject_id,0)

    else:

        j.tryquiz = True
        j.passquiz = False
        session.add(j)
        session.commit()

        hashed_id = j.hashed_id

        text = Markup("""
        You failed the quiz.
        <br><br>
        You total payment is $"""+str(round(j.payment/100, 2))+""".
        <br><br>
        Please enter the following paycode on Amazon M-Turk: 
        <br><br><br>
        <h1>"""+str(hashed_id)+"""</h1>"""
         )

        return render_template('login.html', text=text, v=False)

### landing page.

@app.route('/waitnext/<subject_id>/<rnd>', methods=['POST'])
def WaitNext(subject_id,rnd):

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()
    rnd = int(rnd)

    if rnd == 0:

        text = Markup("""
            <p style="text-align:left;">
            Congratulations! You passed the comprehension quiz and will now move on to the main part of the study.
            <br><br>
            The study consists of """+str(rounds)+""" rounds and in each round, you will have """+str(rndtime) + """ seconds to form <span class=hl>SET</span>s and will be paid an
            additional $0."""+str(j.piecerate)+""" per correct <span class=hl>SET</span>. After  """+str(rounds)+""" rounds, you'll
            be asked to complete a brief survey. Finally, you will receive your Mturk completion code.
            <br><br>
            Any extra amount you earn will be paid via a bonus on MTurk within 3 days.
            <br><br> Click on the SUBMIT button to begin.<p/>""")

        return render_template('login.html', text=text, action=url_for('CreateSets', subject_id=subject_id, rnd=rnd), input=False, v=True)
    
    elif rnd < rounds:

        return render_template('login.html', text='Click SUBMIT to continue to round '+str(rnd+1)+'.', action=url_for('CreateSets', subject_id=subject_id, rnd=rnd), input=False, v=True)

    else:

        return render_template('survey.html', subject_id=subject_id, belief_payment=str(round(belief_payment/100, 2)))

####
#####
######
####### Create Sets Page
######
#####
####

### this generates the page with the cards on it.

@app.route('/createsets/<subject_id>/<rnd>', methods=['POST', 'GET'])
def CreateSets(subject_id,rnd):

        sub = session.query(Subject).all()
        subjectnames = []
        for i in sub:
           subjectnames.append(i.idCode)

        #get list of valid subject names, next we test the input name to
        #sure the imput is valid

        if subject_id not in subjectnames:

            return render_template('login.html', text='Enter a valid subject number.', action='/user_manual', input=True, v=True)

        else:

            ### get SQL object for the subject

            j = session.query(Subject).filter(Subject.idCode == subject_id).one()

            ### we need to start a timer for the subject, or validate against the exisiting timer, if the page
            ### has already been visited (if someone reloads the page---keep timers in the server so that we do
            ### have to deal with people messing with them via JS)

            diff_seconds = rndtime ### global variable for the amound of time the round lasts

            ### if a timer has alread been set for this subject/round, calculate the remaining time

            if session.query(StartTimes).filter(StartTimes.subject == j.id, StartTimes.rnd == rnd).count() > 0:
                exptime = session.query(StartTimes).filter(StartTimes.subject == j.id, StartTimes.rnd == rnd).one()
                diff = exptime.exptime - datetime.now()
                diff = diff - timedelta(microseconds=diff.microseconds)
                diff_seconds = diff.total_seconds()

            ###  otherwise create a new sql entery for the start time
            else:

                new_exptime = StartTimes(
                    subject = j.id,
                    rnd = rnd,
                    exptime = datetime.now() + timedelta(seconds=+rndtime))
                session.add(new_exptime)
                session.commit()

            ###  if there is time remaining

            if diff_seconds < 0:
                
                return render_template('login.html', text='You have already played.', action='/user_manual', v=False)

            elif not j.passquiz:

                return render_template('login.html', text='Sorry, you have failed the quiz', v=False)

            else:

                hand = session.query(HandByRound).filter(HandByRound.subject == j.id, HandByRound.rnd == rnd).one()

                cards = session.query(HandByCard).filter(HandByCard.hand == hand.hand).all()
    
                ###  all the cards in the hand, as HandByCard objects. 

                handarray = []
                handIDarray = []

                ### for each card in the hand, we take its attributes and its unique ID number and store it
                ### of course the attributes define the id, but fuck bijections

                for i in cards:
                    cardsql = session.query(DeckSQL).filter(DeckSQL.id == i.card).one()
                    handarray.append([cardsql.color,cardsql.symbol,cardsql.number])
                    handIDarray.append(cardsql.id)
                
                ### which sets have already been found? 

                foundarray = []
                foundIDarray = []
    
                found = session.query(Found).filter(Found.subject == j.id, Found.rnd == rnd, Found.isset==True, Found.novelset==True).all()
    
                for s in found:
                    setX = session.query(Sets).filter(Sets.id == s.sets).one()
                    card1 = session.query(DeckSQL).filter(DeckSQL.id == setX.card1).one()
                    card2 = session.query(DeckSQL).filter(DeckSQL.id == setX.card2).one()
                    card3 = session.query(DeckSQL).filter(DeckSQL.id == setX.card3).one()
                    foundarray.append([[card1.color,card1.symbol,card1.number],[card2.color,card2.symbol,card2.number],[card3.color,card3.symbol,card3.number]])
                    foundIDarray.append([setX.card1,setX.card2,setX.card3])
    
                found_sets_num = len(foundIDarray)

                rnd = int(rnd)
                next_rnd = rnd + 1
    
                return render_template('set.html', subject_id = subject_id, handarray=handarray, handIDarray=handIDarray, foundarray=foundarray, foundIDarray=foundIDarray, diff_seconds=diff_seconds, found_sets_num=found_sets_num, action=url_for('WaitNext', subject_id=subject_id, rnd=next_rnd),rnd=rnd, time_penalty=time_penalty)

### this next route is just a lil json thing to add new found sets to the database (and keep everything in sync, 
### which is probably unnecessary. so sloppy)


### basically, whats happenin is the browser is sending the server some data. the data is json format, we can 
### request the things we need below (and load them back into python varaibles via json.loads)

@app.route('/_add_set', methods=['POST'])
def AddSetJSON():


    cardsID=request.form['cardsX']
    subject_id=request.form['subject_id']
    isset=request.form['issetX']
    novelset=request.form['novelsetX']
    rnd=request.form['rndX']
    cardsID=json.loads(cardsID)
    isset=json.loads(isset)
    novelset = json.loads(novelset)


    j = session.query(Subject).filter(Subject.idCode == subject_id).one()

    ### isset is a js created varaible do decide if the three cards are a set
    ### if yes, it will find the set as an SQL object. linking the new SQL entry via table join
    ### if no, it will leave newset.sets empty

    ### it reutrns json, but becuase of lazyiness we do not validate on the server side.

    if isset:

        hand = session.query(HandByRound).filter(HandByRound.rnd == int(rnd), HandByRound.subject==j.id).one()

        setX = session.query(Sets).filter(Sets.card1 == cardsID[0], Sets.card2 == cardsID[1], Sets.card3 == cardsID[2], Sets.hand==hand.hand).one()

        newset = Found(
            sets = setX.id,
            subject = j.id,
            timefound = datetime.now(),
            isset = True,
            novelset = novelset,
            rnd = rnd,
            hand = hand.hand)
        session.add(newset)

        if novelset:
            j.payment += j.piecerate
            session.add(j)
        
        session.commit()
    
        return jsonify(foundarray = isset)

    else:

        hand = session.query(HandByRound).filter(HandByRound.rnd == int(rnd), HandByRound.subject==j.id).one()

        newset = Found(
            subject = j.id,
            timefound = datetime.now(),
            isset = False,
            rnd = rnd,
            hand = hand.hand)
        session.add(newset)
        session.commit()
    
        return jsonify(foundarray = isset)

####
#####
######
####### Check Time on Back navigation 
######
#####
####

@app.route('/_check_time', methods=['POST'])
def CheckTimeJSON():

    subject_id=request.form['subject_id']
    rnd=request.form['rndX']

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()


    exptime = session.query(StartTimes).filter(StartTimes.subject == j.id, StartTimes.rnd == rnd).one()
    diff = exptime.exptime - datetime.now()
    diff -= timedelta(microseconds=diff.microseconds)
    diff_seconds = diff.total_seconds()

    return jsonify(reload = (diff_seconds < 0))







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
    guess_prec1 = request.form['percent1']
    guess_prec2 = request.form['percent2']

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()


    #for belief elictation, calc actual precentage
    pos_num = []
    found_num = []
    for i in range(rounds):
        #first which hand
        hand = session.query(HandByRound).filter(HandByRound.rnd == i, HandByRound.subject==j.id).one()
        #next how many total
        pos_num.append(session.query(Sets).filter(Sets.hand == hand.id).count())
        #how many were found
        found_num.append(session.query(Found).filter(Found.subject == j.id, Found.isset == True, Found.novelset == True, Found.rnd == i).count())
        #devide those MFs
        perc_found = [round(x/y,2)*100 for x, y in zip(found_num, pos_num)]


    hashed_id = j.hashed_id

    belief_payment_achived = 0;

    absdiff = [abs(x-y) for x, y in zip(perc_found, [float(guess_prec1),float(guess_prec2)])]
    maxdiff = max(absdiff)
    if maxdiff < 5:
        belief_payment_achived = belief_payment

    j.payment += belief_payment_achived
    j.age = request.form['age']
    j.gender = request.form['gender']
    j.degree = request.form['degree']
    j.percent1 = guess_prec1
    j.percent2 = guess_prec2
    j.bet = request.form['bet']

    session.add(j)
    session.commit()

    text = Markup("""
            Thank you. 
            <br>
            In round 1 you found """+str(found_num[0])+""" of """+str(pos_num[0])+""" sets: """+f'{perc_found[0]:.0f}'+"""%; your assement was """+str(guess_prec1)+"""%. 
            <br>
            In round 2 you found """+str(found_num[1])+""" of """+str(pos_num[1])+""" sets: """+f'{perc_found[1]:.0f}'+"""%; your assement was """+str(guess_prec2)+"""%.
            <br>
            You received a survey bonus of $"""+f'{(round(belief_payment_achived/100, 2)):.2f}'+""".
            <br><br>
            You total payment is $"""+f'{(round(j.payment/100, 2)):.2f}'+""".
            <br><br>
            Please enter the following paycode on Amazon M-Turk: 
            <br><br><br>
            <h1>"""+str(hashed_id)+"""</h1>"""
             )



    return render_template('login.html', text=text, v=False)

             



####
#####
######
####### VIZ
######
#####
####

@app.route('/viz', methods=['POST','get'])
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

 