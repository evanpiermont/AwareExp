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

from db_setup import DeckSQL, Hand, HandByCard, HandByRound, StartTimes, Selection, Subject, Sets, Found, db, app
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
rndtime = 120 #time in seconds
#piecerate = [10,35] #payment in cents per correct anwser
piecerate = [10] #payment in cents per correct anwser
fixed_payment = 50 #fixed payment in cents
belief_payment = 50 #elictation of beliefs bonus payment in cents
rounds = 1 #number of rounds.
time_penalty = 500 #length of penalty in MILIseconds
quizversions = [[1,0,0,1,0],[0,0,1,1,1],[1,1,0,0,1],[0,1,1,1,0]] #list of correct answers for each verison of the quiz 
token_value = 1 #value of token, cents
prize_multiplier = 3 #investment task lottery prize, multiplier


####treatment_aware: 0-2
### 0: Full, (number known ahead of time)
### 1: Surpirse, information revealed after game 
### 2: No-Feedback, infomration not revealed, ambiguity 


####treatment_context: 0-2
### 0: In, (lottery based on number of sets)
### 1: Out, (lottery based on randon number)
### 2: Out, but the subject found 0 sets, so was forced to be in the out group

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


        return render_template('login.html',
            text='Enter a subject number.',
            action='/user_manual',
            input=True,
            v=True)


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

        return render_template('login.html',
            text='Enter a valid subject number.',
            action='/user_manual',
            input=True,
            v=True)

    elif session.query(Subject).filter(Subject.idCode == subject_id).count() == 0:

        hashed_id = hashlib.sha1(subject_id.encode("UTF-8")).hexdigest()[:8]
        q = random.randint(0,len(quizversions)-1) #choose quiz version
        p = random.choice(piecerate)
        t_a = random.randint(0,2) # choose treatment awareness version
        # t_a = 2 # choose treatment awareness version
        t_c = random.randint(0,1) # choose treatment context (cannot chose t_c = 2 (reserved for 0 set finders))
        # t_c = 0 # choose treatment context (cannot chose t_c = 2 (reserved for 0 set finders))

        treatment_version = "xx" + str(t_a) + "xx" + str(t_c)
       
        subject = Subject(
            idCode= subject_id,
            hashed_id = hashed_id,
            quizversion = q,
            piecerate = p,
            payment = fixed_payment,
            asset_numerator = 0,
            treatment_aware = t_a,
            treatment_context = t_c)    
        session.add(subject)
        session.commit()
        hands = session.query(Hand).all() #all possible hands
        random.seed(datetime.now())
        handarray = random.sample(hands, rounds) #random sample, 1 for each round
        j = session.query(Subject).filter(Subject.idCode == subject_id).one()
        
        for rnd in range(rounds):
            new_hand_by_round = HandByRound(
                subject = j.id,
                rnd = rnd+1,
                hand = handarray[rnd].id)
            session.add(new_hand_by_round)
            session.commit()

        return render_template('instructions.html',
            subject_id = subject_id, 
            piecerate=f'{round(p/100, 2):.2f}', 
            rounds=str(rounds), 
            fixed_payment=f'{round(fixed_payment/100, 2):.2f}',
            treatment_version = treatment_version)
        #return Quiz(subject_id) 
    else:
            return render_template('login.html',
                text='You have already played.',
                action='/user_manual',
                v=False)




### just routes the guy to the quiz. we could obviously totally get around this by formatting URLS
### and just making the redirect from the instructions directly. but why not. 

@app.route('/compquiz/<subject_id>', methods=['POST', 'GET'])
def Quiz(subject_id):

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()


    if j.tryquiz:

        return render_template('login.html',
            text='You have already failed the quiz.',
            input=False,
            v=False)

    else:
        q = j.quizversion
        return render_template('quiz.html',
            subject_id = subject_id,
            q=q)

### now we need to make sure they passed the quiz. 

@app.route('/quizval', methods=['POST'])
def QuizVal():

    subject_id=str(request.form['subject_id'])
    j = session.query(Subject).filter(Subject.idCode == subject_id).one()


    if j.tryquiz:
        return render_template('login.html',
            text='You have already failed the quiz.',
            input=False, v=False)

    quiz_ans=[int(request.form['set1']),
              int(request.form['set2']),
              int(request.form['set3']),
              int(request.form['set4']),
              int(request.form['set5'])]
    correct = quizversions[j.quizversion]

    num_correct = [(x+y)%2 for x, y in zip(quiz_ans, correct)].count(0)
 
    if num_correct > 3:

        j.tryquiz = True
        j.passquiz = num_correct
        session.add(j)
        session.commit()

        return WaitNext(subject_id,0)

    else:

        j.tryquiz = True
        j.passquiz = num_correct
        session.add(j)
        session.commit()

        hashed_id = j.hashed_id

        text = Markup("""
        You failed the quiz.
        <br><br>
        You total payment is $"""+f'{round(j.payment/100, 2):.2f}'+""".
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
    next_rnd = rnd + 1

    if rnd == 0:

        text = Markup("""
            <p style="text-align:left;">
            Congratulations! You passed the comprehension quiz and will move on to the main part of the study.
            <br><br>
            In Task 1 you will have """+str(rndtime) + """ seconds to form <span class=hl>SET</span>s. You will be paid an
            additional $"""+f'{round(j.piecerate/100, 2):.2f}'+""" per correct <span class=hl>SET</span>.
            <br><br>
            After completing Task 1 you will receive instructions for Task 2. Following Task 2, you will be asked to answer
            a few survey questions. Finally, you will receive your Mturk completion code.
            <br><br>
            Any extra amount you earn will be paid via a bonus on MTurk within 5 days.
            <br><br> Click on the SUBMIT button to begin.<p/>""")

        return render_template('login.html',
            text=text, 
            action=url_for('CreateSets', subject_id=subject_id, rnd=next_rnd), 
            input=False, 
            v=True)
    
    #multi round issues:: not needed for current setup
    # elif rnd < rounds:

    #     j.percent1 = request.form['percent']
    #     session.add(j)
    #     session.commit()

    #     text = Markup("""
    #         Click SUBMIT to continue to round """+str(next_rnd)+""".
    #         """)
    #     return render_template('login.html',
    #         text=text,
    #         action=url_for('CreateSets', 
    #             subject_id=subject_id,
    #             rnd=next_rnd),
    #         input=False,
    #         v=True)

    elif rnd == 1:





        t_a = j.treatment_aware
        num = j.asset_numerator

        j.belief = request.form['percent']
        session.add(j)
        session.commit()

        if num==0:
            j.treatment_context = 2
            session.add(j)
            session.commit()

        #create sets array for feedback screen
        #here we also create the 'selection' table with the sets that will be chosen from
        #later in the risk elicitation. 

        setarray = []
        selection_array = []
        not_found_array = []
        
        #get the hand of the individual, then the list of all sets
        hand = session.query(HandByRound).filter(HandByRound.subject == j.id,
                                                 HandByRound.rnd == rnd).one()
        sets = session.query(Sets).filter(Sets.hand == hand.hand).all()

        #get number of sets, for now this is always 28, but might be diff later

        sets_len = len(sets)

        #how many sets to find

        select_len = sets_len

        if num < (sets_len / 2):
            select_len = num*2


        for s in sets:
                card1 = session.query(DeckSQL).filter(DeckSQL.id == s.card1).one()
                card2 = session.query(DeckSQL).filter(DeckSQL.id == s.card2).one()
                card3 = session.query(DeckSQL).filter(DeckSQL.id == s.card3).one()
    
                found = session.query(Found).filter(Found.subject == j.id,
                                                    Found.rnd == 1,
                                                    Found.isset==True,
                                                    Found.novelset==True,
                                                    Found.sets==s.id).count()
                if found:
                    #add to setarray to be displayed in feedback
                    setarray.append([
                        [card1.color,card1.symbol,card1.number],
                        [card2.color,card2.symbol,card2.number],
                        [card3.color,card3.symbol,card3.number],
                        1])
                else:
                    setarray.append([
                        [card1.color,card1.symbol,card1.number],
                        [card2.color,card2.symbol,card2.number],
                        [card3.color,card3.symbol,card3.number],
                        0])
                    #potentials to add to table so that it can be used for lottery construction.
                    not_found_array.append(s)

        #make sure we havent done this before (then there would be falses)
        is_selected = session.query(Selection).filter(Selection.subject == j.id,
                                                      Selection.found==False).count()
        if not is_selected:
            #take a selection of the not found ones for lottery
            not_found_array = random.choices(not_found_array, k=select_len - num)

            for s in not_found_array:
                select = Selection(
                    sets = s.id,
                    subject = j.id,
                    found = False)
                session.add(select)
                session.commit()




        #set feeback text based on treatement, 
        #the 'feedback' boolean also controls if the subject sees all sets.

        feedback = True # reveal feedback; true for treatment 0,1

        if t_a == 2: 
            feedback = False

        if feedback:
            den = j.asset_denominator
            text = "You found " + str(num) + " out of " + str(den) + " sets."
        else:
            text = "You found " + str(num) + " sets. Please continue to Task 2."

        return render_template('feedback.html',
            text=text, 
            action=url_for('RiskElicit', subject_id=subject_id, rnd=next_rnd), 
            setarray = setarray,
            feedback = feedback,
            )

    else:
        text = Markup("""
            The study is over.
            """)

        return render_template('login.html',
            text=text, 
            action=url_for('Survey', 
                subject_id=subject_id,  
                belief_payment=belief_payment), 
            input=False, v=False)


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

            return render_template('login.html',
                text='Enter a valid subject number.',
                action='/user_manual',
                input=True,
                v=True)

        else:

            ### get SQL object for the subject

            j = session.query(Subject).filter(Subject.idCode == subject_id).one()

            ### we need to start a timer for the subject, or validate against the exisiting timer, if the page
            ### has already been visited (if someone reloads the page---keep timers in the server so that we do
            ### have to deal with people messing with them via JS)

            diff_seconds = rndtime ### global variable for the amound of time the round lasts

            ### if a timer has alread been set for this subject/round, calculate the remaining time

            if session.query(StartTimes).filter(StartTimes.subject == j.id,
                                                StartTimes.rnd == rnd).count() > 0:
                exptime = session.query(StartTimes).filter(StartTimes.subject == j.id,
                                                           StartTimes.rnd == rnd).one()
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
                
                return render_template('login.html',
                    text='You have already played.',
                    action='/user_manual',
                    v=False)

            elif j.passquiz < 4:

                return render_template('login.html',
                    text='Sorry, you have failed the quiz',
                    v=False)

            else:

                hand = session.query(HandByRound).filter(HandByRound.subject == j.id,
                                                         HandByRound.rnd == rnd).one()
                sets = session.query(Sets).filter(Sets.hand == hand.hand).all()

                #enter how many sets there are in total
                den = len(sets)
                j.asset_denominator = den
                session.add(j)
                session.commit()
                

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
    
                found = session.query(Found).filter(Found.subject == j.id,
                    Found.rnd == rnd,
                    Found.isset==True,
                    Found.novelset==True).all()
    
                for s in found:
                    setX = session.query(Sets).filter(Sets.id == s.sets).one()
                    card1 = session.query(DeckSQL).filter(DeckSQL.id == setX.card1).one()
                    card2 = session.query(DeckSQL).filter(DeckSQL.id == setX.card2).one()
                    card3 = session.query(DeckSQL).filter(DeckSQL.id == setX.card3).one()
                    foundarray.append([[card1.color,card1.symbol,card1.number],
                                       [card2.color,card2.symbol,card2.number],
                                       [card3.color,card3.symbol,card3.number]])
                    foundIDarray.append([setX.card1,setX.card2,setX.card3])
    
                found_sets_num = len(foundIDarray)

                t_a = j.treatment_aware
                aware = False #if aware the full awareness treatment, i.e, 0
                if t_a == 0:
                    aware = True
                    

                return render_template('set.html', 
                    subject_id = subject_id, 
                    handarray=handarray, 
                    handIDarray=handIDarray, 
                    foundarray=foundarray, 
                    foundIDarray=foundIDarray, 
                    diff_seconds=diff_seconds, 
                    found_sets_num=found_sets_num, 
                    action=url_for('BeliefElicit', subject_id=subject_id, rnd=rnd),
                    rnd=rnd,
                    time_penalty=time_penalty,
                    end_survey=True,
                    aware=aware,
                    den=den)


####belief elicitation page
@app.route('/be/<subject_id>/<rnd>', methods=['POST'])
def BeliefElicit(subject_id,rnd):

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()
    rnd = int(rnd)

    num = j.asset_numerator
    t_a = j.treatment_aware

    aware = True
    if t_a > 0: #if not the full aware group (they do not do the elicitation method)
        aware = False

    return render_template('survey.html',
        subject_id=subject_id,
        end_survey = False,
        num =num,
        be = True,
        aware = aware,
        action=url_for('WaitNext', subject_id=subject_id, rnd=rnd),)



####risk elicitation page
@app.route('/re/<subject_id>/<rnd>', methods=['POST'])
def RiskElicit(subject_id,rnd):

    rnd = int(rnd)

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()

    t_a = j.treatment_aware
    t_c = j.treatment_context
    num = j.asset_numerator
    den = j.asset_denominator
    #prob = int((num*100)/den)
    #exogenously set prob of winning to .5
    prob = 50

    feedback = True # reveal feedback; true for treatment 0,1

    if t_a == 2: 
        feedback = False

    context = True # true == in context, based on sets

    if t_c > 0: #i.e, t_c is treatment 1 or 2
        context = False #false == out of context, based on random number

    #construct slection for lottery
    sel_array = []
    selection = session.query(Selection).filter(Selection.subject == j.id).all()
    select_len = len(selection)
    for s in selection:
        found_set = session.query(Sets).filter(Sets.id == s.sets).one()
        card1 = session.query(DeckSQL).filter(DeckSQL.id == found_set.card1).one()
        card2 = session.query(DeckSQL).filter(DeckSQL.id == found_set.card2).one()
        card3 = session.query(DeckSQL).filter(DeckSQL.id == found_set.card3).one()
        if s.found:       
            sel_array.append([
                [card1.color,card1.symbol,card1.number],
                [card2.color,card2.symbol,card2.number],
                [card3.color,card3.symbol,card3.number],
                1])
        else:
            sel_array.append([
                [card1.color,card1.symbol,card1.number],
                [card2.color,card2.symbol,card2.number],
                [card3.color,card3.symbol,card3.number],
                0])

    random.shuffle(sel_array)

    unaware = False #dummy for unawareness treatment, i.e, 2
    if t_a == 2:
        unaware = True

    return render_template('risk.html', 
        subject_id=subject_id, 
        #belief_payment=f'{(round(int(belief_payment)/100, 2)):.2f}', 
        action=url_for('Survey',subject_id=subject_id,),
        rnd=rnd,
        prize_multiplier = prize_multiplier,
        token_value = token_value,
        feedback=feedback,
        context=context,
        sel_array=sel_array,
        select_len=select_len,
        num=num,
        den=den,
        unaware=unaware,
        prob=prob)


@app.route('/_is_mobile', methods=['POST'])
def isMobile():

    subject_id=request.form['subject_id']
    isMobile=request.form['isMobileX']

    isMobile = int(isMobile)

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()
    j.mobile = isMobile

    session.add(j)
    session.commit()
    
    return('set_mobile')



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

        hand = session.query(HandByRound).filter(HandByRound.rnd == int(rnd),
                                                 HandByRound.subject==j.id).one()

        setX = session.query(Sets).filter(Sets.card1 == cardsID[0],
                                          Sets.card2 == cardsID[1],
                                          Sets.card3 == cardsID[2],
                                          Sets.hand==hand.hand).one()

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
            j.asset_numerator += 1
            session.add(j)

            #add to slection table, for lottery construction.
            select = Selection(
                sets = setX.id,
                subject = j.id,
                found = True)
            session.add(select)
            session.commit()
        
        session.commit()
    
        return jsonify(foundarray = isset)

    else:

        hand = session.query(HandByRound).filter(HandByRound.rnd == int(rnd),
                                                 HandByRound.subject==j.id).one()

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


    exptime = session.query(StartTimes).filter(StartTimes.subject == j.id,
                                               StartTimes.rnd == rnd).one()
    diff = exptime.exptime - datetime.now()
    diff -= timedelta(microseconds=diff.microseconds)
    diff_seconds = diff.total_seconds()

    return jsonify(reload = (diff_seconds < 0))


####
#####
######
####### Check Time on Back navigation 
######
#####
####

@app.route('/survey/<subject_id>', methods=['POST', 'GET'])
def Survey(subject_id,):

    j = session.query(Subject).filter(Subject.idCode == subject_id).one()

    j.risk_aversion = request.form['percent']
    session.add(j)
    session.commit()

    return render_template('survey.html',
        subject_id=subject_id,
        end_survey = True,
        action='/end')





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


    # #for belief elictation, calc actual precentage
    # pos_num = []
    # found_num = []
    # for i in range(rounds):
    #     i+=1
    #     #first which hand (is a HandByRound thing, so we need to take the .hand of it to get the hand id)
    #     hand = session.query(HandByRound).filter(HandByRound.rnd == i, HandByRound.subject==j.id).one()
    #     #next how many total
    #     pos_num.append(session.query(Sets).filter(Sets.hand == hand.hand).count())
    #     #how many were found
    #     found_num.append(session.query(Found).filter(Found.subject == j.id, Found.isset == True, Found.novelset == True, Found.rnd == i).count())
    #     #devide those MFs
    #     perc_found = [round(x/y,2)*100 for x, y in zip(found_num, pos_num)]



    # belief_payment_achived = 0;

    # absdiff = [abs(x-y) for x, y in zip(perc_found, [float(guess_prec1),float(guess_prec2)])]
    # mindiff = min(absdiff)
    # if mindiff <= 5:
    #     belief_payment_achived = belief_payment

    j.age = request.form['age']
    j.gender = request.form['gender']
    j.degree = request.form['degree']

    session.add(j)
    session.commit()

    hashed_id = j.hashed_id


    text = Markup("""
            Thank you!
            <br><br>
            Any bonus payments will be made within 5 days.
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

 
