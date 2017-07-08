from flask import Flask, request, redirect, url_for, render_template, jsonify
app = Flask(__name__)

import os
import datetime, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from random import randint

from db_setup import LetterBank, FoundWords, WordBank, Subject, Contracts, BDMLines, SubjectLetterBank, DataBDM, Base, TimeStarted, ChosenOnes, DOSEGambles

import cgi
import collections


filePath = os.getcwd()
engine = create_engine('sqlite:///'+ filePath + '/restaurantmenu.db')

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
####### Round Page, goes to contract if round is even, and to word finder if round is odd 
######
#####
####

@app.route('/wait_for_first_round', methods=['POST'])
def waitForFirstRound():

 
        subject_id=request.form['subject_id']
        cr=request.form['current_round']


        sub = session.query(Subject).all()
        subjectnames = []
        for i in sub:
           subjectnames.append(i.subject_name)

        #get list of valid subject names, next we test the input name to
        #sure the imput is valid

        if subject_id == "admin.faep":

            return render_template('admin_create.html')

        elif subject_id in subjectnames:

            j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

            xid = j.id

            j.wait_end_session = False
            j.wait_for_delay_entry = False
            j.wait_for_word_urn = False
            session.add(j)
            session.commit()
            
            return render_template('wait_bdm.html', subject_id = subject_id, task=False, nextr=False, cr=cr, nextaction="/round", wait_time=.25)

        else:
            return render_template('login.html', v=False)

@app.route('/round', methods=['POST'])
def NewRound():

        subject_id=request.form['subject_id'].lower()
        cr=request.form['current_round']
        cr = int(cr) + 1 
        #get subject id, this follows the subject for the duration
        #get the previous round, add one.


        #delete all old timestamps: this is for debugging. 
        #create a timestamp entry in the TimeStarted table to act as a
        # reference for wait time

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        xid = j.id

        session.query(TimeStarted).filter(TimeStarted.subject_id == xid).filter(TimeStarted.rnd == cr).filter(TimeStarted.task == 1).delete()

        timestamp = TimeStarted(rnd = cr, task =1, subject = j)
        session.add(timestamp)
        session.commit()

        #get timestamp for begining of round

        ts = session.query(TimeStarted).join(Subject).filter(Subject.subject_name == subject_id).filter(TimeStarted.rnd == cr).filter(TimeStarted.task == 1).one()
        #convert to useable JS

        tsjs = int(time.mktime(ts.start_time.timetuple())) * 1000

        q = session.query(LetterBank).filter(LetterBank.subjects.any(subject_id=xid)).filter(LetterBank.subjects.any(rnd=cr, task=1)).one()

        return render_template('scrabble.html', q=q, subject_id = subject_id, cr = cr, v=False, tsjs = tsjs) 


###
#####
######
####### TASK 2
######
#####
####


@app.route('/task2', methods=['POST'])
def MoveToTask2():

        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        #get the current suject bets

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        xid = j.id
        

        #delete all old timestamps: this is for debugging. 
        #create a timestamp entry in the TimeStarted table to act as a
        # reference for wait times

        session.query(TimeStarted).filter(TimeStarted.subject_id == xid).filter(TimeStarted.rnd == cr).filter(TimeStarted.task == 2).delete()

        timestamp = TimeStarted(rnd = cr, subject = j, task=2)
        session.add(timestamp)
        session.commit()

        #get timestamp for begining of round

        ts = session.query(TimeStarted).join(Subject).filter(Subject.subject_name == subject_id).filter(TimeStarted.rnd == cr).filter(TimeStarted.task == 2).one()
        #convert to useable JS

        tsjs = int(time.mktime(ts.start_time.timetuple())) * 1000

        bets = collections.OrderedDict()
        bets['A'] = [2,14]
        bets['B'] = [14,2]
        bets['C'] = [6,6]


        q = session.query(LetterBank).filter(LetterBank.subjects.any(subject_id=xid)).filter(LetterBank.subjects.any(rnd=cr, task=2)).one()

        return render_template('contracts.html', q=q, subject_id = subject_id, v=False, bets=bets, cr = cr, tsjs = tsjs)



####
#####
######
####### FIND WORDS PAGE,
######
#####
####




@app.route('/word', methods=['POST'])
def WordPage():

        subject_id=request.form['subject_id']
        newWord=request.form['word']
        cr=request.form['current_round']

        v = False # if true displays found words,
        v2 = False #if true displays, XXX is not a word
        v3 = False #if true displays, you already found XXX

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        xid = j.id

        q = session.query(LetterBank).filter(LetterBank.subjects.any(subject_id=xid)).filter(LetterBank.subjects.any(rnd=cr, task=1)).one()

        ts = session.query(TimeStarted).join(Subject).filter(Subject.subject_name == subject_id).filter(TimeStarted.rnd == cr).filter(TimeStarted.task == 1).one()
            #convert to useable JS

        tsjs = int(time.mktime(ts.start_time.timetuple())) * 1000


        currentWordBank = session.query(WordBank).join(LetterBank).filter(LetterBank.name == q.name).all()
        qfw = session.query(FoundWords).filter(FoundWords.subject == subject_id).filter(FoundWords.current_round == cr).all()
               
        cwb = [] #list of the current word bank
        fwl = [] #list of previously found words by user
                        
        for item in currentWordBank:
            cwb.append(item.word)
                            
        for item in qfw:
            fwl.append(item.word)
        
        
        if newWord in cwb: #make sure that the content is a valid word, save if yes(valid=true), if no (valid = Flase)
            if newWord not in fwl: #make sure the content is not a duplicate
                found1 = FoundWords(word = newWord, subject = subject_id, current_round = cr, valid=True) #commits the found word
                session.add(found1)
                session.commit()
            else:
                v3 = True
        else:
            found2 = FoundWords(word = newWord, subject = subject_id, current_round = cr, valid=False)
            session.add(found2)
            session.commit()
            v2 = True
        
        fw = [] 
        qfw = session.query(FoundWords).filter(FoundWords.subject == subject_id).filter(FoundWords.current_round == cr).filter(FoundWords.valid== True).all() #outputs all current found and valid words
        
        for item in qfw:
            fw.append(item.word.upper())
            v = True


        return render_template('scrabble.html', q=q, subject_id = subject_id, v=v, fw=fw, cr=cr, v2=v2, v3=v3, tsjs=tsjs, lastWord=newWord) 

####
#####
######
####### CREATE CONTRACTS PAGE, with contracts listed
######
#####
####


@app.route('/contract', methods=['POST'])
def ContractPage():

        subject_id=request.form['subject_id']
        newWord=request.form['word']
        b4u1=request.form['current_bet_urn_1']
        b4u2=request.form['current_bet_urn_2']
        cr=request.form['current_round']

        #get current subject and id

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        xid = j.id

        #get timestamp for begining of round

        ts = session.query(TimeStarted).join(Subject).filter(Subject.subject_name == subject_id).filter(TimeStarted.rnd == cr).filter(TimeStarted.task == 2).one()
        #convert to useable JS

        tsjs = int(time.mktime(ts.start_time.timetuple())) * 1000

        #get current letterbank for subject by round
        
        q = session.query(LetterBank).filter(LetterBank.subjects.any(subject_id=xid)).filter(LetterBank.subjects.any(rnd=cr, task=2)).one()

        currentWordBank = session.query(WordBank).join(LetterBank).filter(LetterBank.name == q.name).all()
        qfw = session.query(FoundWords).filter(FoundWords.subject == subject_id).filter(FoundWords.current_round == cr).all()
               
        cwb = [] #list of the current word bank

        for item in currentWordBank:
            cwb.append(item.word)
 
        bets = collections.OrderedDict()
        bets['A'] = [2,14]
        bets['B'] = [14,2]
        bets['C'] = [6,6]

        #get the list of previously entered contracts, if they are being displayed
        oc = session.query(Contracts).filter(Contracts.subject == subject_id).filter(Contracts.display == True).filter(Contracts.current_round == cr).all()

        ccList = [] #list of the current contracts

        for item in oc:
            ccList.append(item.word)

        if newWord in cwb:

            if newWord not in ccList:
                contract = Contracts(word = newWord, bet1 = b4u1, bet2 = b4u2, subject = subject_id, current_round = cr, valid=True)
                session.add(contract)
                session.commit()
            else:
               overwrite =  session.query(Contracts).filter(Contracts.subject == subject_id).filter(Contracts.display == True).filter(  Contracts.word == newWord).filter(Contracts.current_round == cr).one()
               overwrite.display = False
               session.add(overwrite)
               contract = Contracts(word = newWord, bet1 = b4u1, bet2 = b4u2, subject =
                                  subject_id, current_round = cr, valid=True)
               session.add(contract)
               session.commit()
    
            cc = session.query(Contracts).filter(Contracts.subject == subject_id).filter(Contracts.display == True).filter(Contracts.valid == True).filter(Contracts.current_round == cr).all()
    
            return render_template('contracts.html', q=q, subject_id = subject_id, v=True, v2=False, bets=bets, cr=cr, cc=cc, tsjs=tsjs)
        else:

            cc = session.query(Contracts).filter(Contracts.subject == subject_id).filter(Contracts.display == True).filter(Contracts.valid == True).filter(Contracts.current_round == cr).all()

            contract = Contracts(word = newWord, bet1 = b4u1, bet2 = b4u2, subject = subject_id, current_round = cr, valid=False)
            session.add(contract)
            session.commit()


            return render_template('contracts.html', q=q, subject_id = subject_id, lastWord=newWord, v=True, v2=True, bets=bets, cr=cr, cc=cc, tsjs=tsjs)

####
#####
######
####### BDM PAGE
######
#####
####



@app.route('/bdm', methods=['GET', 'POST'])
def BDMPage():

 
        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        lines = session.query(BDMLines).all()
        #get the current suject

        return render_template('bdm.html', subject_id = subject_id, cr=cr, lines=lines)



####
#####
######
####### SCRABBLE FEEDBACK PAGE
######
#####
####


@app.route('/scrabble_feedback', methods=['GET', 'POST'])
def SFeedBackPage():

    if request.method == 'POST':
        subject_id=request.form['subject_id']
        cr=request.form['current_round']
        v = False
        v2 = False

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        xid = j.id

        q = session.query(LetterBank).filter(LetterBank.subjects.any(subject_id=xid)).filter(LetterBank.subjects.any(rnd=cr, task=1)).one()


        currentWordBank = session.query(WordBank).join(LetterBank).filter(LetterBank.name == q.name).all()
        fw = session.query(FoundWords).filter(FoundWords.subject == subject_id).filter(FoundWords.current_round == cr).filter(FoundWords.valid == True).all()

               
        cwb = [] #list of the current word bank
        fwl = [] #list of previously found words by user
                        
        for item in currentWordBank:
            cwb.append(item.word)
                            
        for item in fw:
            fwl.append(item.word)
        
        cwb2 = set(cwb) - set(fwl)

        if not cwb2:
            v = True

        if j.treatment == 1: # treatment = 1 is no feedback on the scrabble task
            v2 = True

        return render_template('scrabble_feedback.html', q=q, subject_id = subject_id, v=v, v2=v2, fwl=fwl, cwb2=cwb2, cr=cr) 
    else:
        return render_template('login.html', v=True)

####
#####
######
####### controling holdup of users
######
#####
####

####
#####
######
####### Wait PAGES and checks
######
#####
####

@app.route('/wait_bdm', methods=['POST'])
def BDMwaitPage():

 
        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        # enter bdm info into DB

        lines = session.query(BDMLines).all()

        for line in lines:
            resultForLine = request.form[line.line_name]
            newBDMdata = DataBDM(rnd = cr, subject = j, bdm_lines = line, contract_or_delay = resultForLine)
            session.add(newBDMdata)
            session.commit()

        if int(cr) < 1: #user has more rounds to go ### CHANGE

            #set users wait to false becuase they are not done 

            j.last_round_completed = int(cr)
            j.wait_end_session = False
            j.wait_for_delay_entry = False
            j.wait_for_word_urn = False
            session.add(j)
            session.commit()

            return render_template('wait.html', subject_id = subject_id, cr=cr, nextaction = "/wait_for_next_round", waitCheckNum = "/_waitCheckRoundEnd", message = "for other users to reach this stage")
                                 
        else:

            # user is done, change wait to true, so we can continute
            j.wait_end_session = True
            session.add(j)
            session.commit()

            return render_template('wait.html', subject_id = subject_id, cr=cr, nextaction = "/results_task1", waitCheckNum = "/_waitCheckNum1", message = "for the random round to be drawn")


@app.route('/wait_for_task2', methods=['POST'])
def waitForTask2():

 
        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        # enter bdm info into DB

        lines = session.query(BDMLines).all()


        #set users wait to false becuase they are not done

        j.wait_end_session = False
        j.wait_for_delay_entry = False
        j.wait_for_word_urn = False
        session.add(j)
        session.commit()

        return render_template('wait_bdm.html', subject_id = subject_id, task=True, nextr=True, cr=cr, nextaction="/task2", wait_time=.2)

@app.route('/wait_for_next_round', methods=['POST'])
def waitForNextRound():

 
        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        return render_template('wait_bdm.html', subject_id = subject_id, task=False, nextr=True, cr=cr, nextaction="/round", wait_time=.5)
                                 

@app.route('/wait_to_draw_urn', methods=['POST'])
def waitResultsPage3():

 
        subject_id=request.form['subject_id']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        # enter bdm info into DB

        j.wait_for_word_urn = True
        session.add(j)
        session.commit()

        return render_template('wait.html', subject_id = subject_id, nextaction = "/results", waitCheckNum = "/_waitCheckNum2", message = "for the random word, line, and urn to be drawn")


@app.route('/wait_results_2', methods=['POST'])
def waitResultsPage2():

 
        subject_id=request.form['subject_id']
        CorD=request.form['CorD']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        # enter bdm info into DB

        j.wait_for_delay_entry = True
        session.add(j)
        session.commit()

        if CorD == "Delay":
            realized_bet = request.form['realized_bet']
            j.realized_bet = realized_bet
            session.add(j)
            session.commit()

        return render_template('wait.html', subject_id = subject_id, nextaction = "/results_for_ball", waitCheckNum = "/_waitCheckNum3", message = "for the random ball to be drawn from the selected urn")

@app.route('/wait_end_part_1', methods=['POST'])
def waitEndPart1():

 
        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

        return render_template('wait.html', subject_id = subject_id, nextaction = "/risk_e", waitCheckNum = "/_waitCheckEndPart1", message = "for the instuctions for part 2")


@app.route('/_waitCheckNum1')
def WaitCheckJSON():

    chosen = session.query(ChosenOnes).order_by(ChosenOnes.id.desc()).first()

    subs = session.query(Subject).all()
    v = chosen.wait_end_session

    for i in subs:
        v = v and i.wait_end_session

    if v:
        return jsonify(txt = 'go')
    else:
        return jsonify(txt = 'stop')

@app.route('/_waitCheckNum2')
def WaitCheck2JSON():

    chosen = session.query(ChosenOnes).order_by(ChosenOnes.id.desc()).first()

    v = chosen.wait_for_word_urn
    
    if v:
        return jsonify(txt = 'go')
    else:
        return jsonify(txt = 'stop')


@app.route('/_waitCheckNum3')
def WaitCheck3JSON():

	chosen = session.query(ChosenOnes).order_by(ChosenOnes.id.desc()).first()

	subs = session.query(Subject).all()
	v = chosen.wait_for_delay_entry

	for i in subs:
		v = v and i.wait_for_delay_entry
	
	if v:
		return jsonify(txt = 'go')
	else:
		return jsonify(txt = 'stop')

@app.route('/_waitCheckRoundEnd')
def WaitCheckRoundJSON():

    subs = session.query(Subject).filter(Subject.wait_end_session == False).all()

    rndbysubject = []
    for i in subs:
        rndbysubject.append(i.last_round_completed)

    v = (len(set(rndbysubject)) <= 1)   

    if v:
        return jsonify(txt = 'go')
    else:
        return jsonify(txt = 'stop')


@app.route('/_waitCheckEndPart1')
def WaitCheckPart1JSON():
    
    chosen = session.query(ChosenOnes).order_by(ChosenOnes.id.desc()).first()
    v= chosen.wait_for_part_2  

    if v:
        return jsonify(txt = 'go')
    else:
        return jsonify(txt = 'stop')


####
#####
######
####### Results, TASK 1
######
#####
####



@app.route('/results_task1', methods=['POST'])
def Task1ResultsPage():

        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        xid = j.id
        session_no = j.session_no

        chosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()

        fwc = len(session.query(FoundWords).filter(FoundWords.subject == subject_id).filter(FoundWords.current_round == chosen.rnd).filter(FoundWords.valid == True).all())

        earnings = fwc*.5

        current_earnings = j.totalearnings

        j.earnings_task1 = earnings
        j.totalearnings = current_earnings + earnings
        session.add(j)
        session.commit()

        return render_template('results_task1.html', chosen = chosen, fwc=fwc, earnings=earnings, subject_id = subject_id)



####
#####
######
####### Results, Page 1
######
#####
####



@app.route('/results', methods=['POST'])
def EndResultsPage():

        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        xid = j.id
        session_no = j.session_no

        chosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()

        CorD = session.query(DataBDM).filter(DataBDM.rnd == chosen.rnd).join(Subject).filter(Subject.id == xid).join(BDMLines).filter(BDMLines.line_number == chosen.line).order_by(DataBDM.id.desc()).first()

        line = session.query(BDMLines).filter(BDMLines.line_number == chosen.line).one()

        bonus = line.contract_bonus

        if CorD.contract_or_delay == 'D':
            bonus = line.delay_bonus

        current_earnings = j.earnings_task1 + bonus

        j.earnings_bonus = bonus
        j.totalearnings = current_earnings
        session.add(j)
        session.commit()


        return render_template('results.html', chosen = chosen, CorD = CorD, cr=cr, line=line, current_earnings=current_earnings, subject_id = subject_id)


####
#####
######
####### Results, Contract Realization
######
#####
####



@app.route('/results_contract', methods=['POST'])
def EndResultsPageContract():

        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        xid = j.id
        session_no = j.session_no

        bets = collections.OrderedDict()
        bets['A'] = [2,14]
        bets['B'] = [14,2]
        bets['C'] = [6,6]
        bets['X'] = [5,5] 

        chosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()

        CorD = session.query(DataBDM).filter(DataBDM.rnd == chosen.rnd).join(Subject).filter(Subject.id == xid).join(BDMLines).filter(BDMLines.line_number == chosen.line).order_by(DataBDM.id.desc()).first()

        line = session.query(BDMLines).filter(BDMLines.line_number == chosen.line).one()

        bonus = line.contract_bonus

        if CorD.contract_or_delay == 'D':
            bonus = line.delay_bonus

        urnchoice = "Heads"
        
        if chosen.urn == 2:
            urnchoice = "Tails"

        current_earnings = j.totalearnings


        xxcontract = session.query(Contracts).filter(Contracts.subject == subject_id).filter(Contracts.display == True).filter(Contracts.word == chosen.word).filter(Contracts.current_round == chosen.rnd).all()

        if xxcontract: #checks if list of contracts is non-empty, then computes realized bet
            realContract = session.query(Contracts).filter(Contracts.subject == subject_id).filter(Contracts.display == True).filter(Contracts.word == chosen.word).filter(Contracts.current_round == chosen.rnd).one()
            xxbets = [realContract.bet1, realContract.bet2]
            j.realized_bet = xxbets[chosen.urn - 1]
            session.add(j)
            session.commit()
        else:
            realContract = 'X'
            j.realized_bet = 'X'
            session.add(j)
            session.commit()
        

        return render_template('results_contract.html', chosen = chosen, CorD = CorD, cr=cr, line=line, current_earnings=current_earnings, subject_id = subject_id, urnchoice=urnchoice, realContract=realContract, bets=bets, realized_bet=j.realized_bet)

@app.route('/results_delay', methods=['POST'])
def EndResultsPageDelay():

        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        xid = j.id
        session_no = j.session_no

        bets = collections.OrderedDict()
        bets['A'] = [2,15]
        bets['B'] = [14,2]
        bets['C'] = [6,6]
        bets['X'] = [5,5]  


        chosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()

        CorD = session.query(DataBDM).filter(DataBDM.rnd == chosen.rnd).join(Subject).filter(Subject.id == xid).join(BDMLines).filter(BDMLines.line_number == chosen.line).order_by(DataBDM.id.desc()).first()

        line = session.query(BDMLines).filter(BDMLines.line_number == chosen.line).one()

        bonus = line.contract_bonus

        if CorD.contract_or_delay == 'D':
            bonus = line.delay_bonus

        urnchoice = "Heads"
        if chosen.urn == 2:
            urnchoice = "Tails"


        return render_template('results_delay.html', chosen = chosen, urnchoice=urnchoice, CorD = CorD, cr=cr, line=line, bonus=bonus, subject_id = subject_id, bets=bets)

@app.route('/results_for_ball', methods=['POST'])
def BallResultsPageContract():

        subject_id=request.form['subject_id']
        cr=request.form['current_round']

        j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
        xid = j.id
        session_no = j.session_no

        bets = collections.OrderedDict()
        bets['A'] = [2,14]
        bets['B'] = [14,2]
        bets['C'] = [6,6]
        bets['X'] = [5,5] 

        chosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()

        CorD = session.query(DataBDM).filter(DataBDM.rnd == chosen.rnd).join(Subject).filter(Subject.id == xid).join(BDMLines).filter(BDMLines.line_number == chosen.line).order_by(DataBDM.id.desc()).first()

        line = session.query(BDMLines).filter(BDMLines.line_number == chosen.line).one()

        bonus = line.contract_bonus

        if CorD.contract_or_delay == 'D':
            bonus = line.delay_bonus

        ballColor = "Yellow"

        if chosen.ball == 2:
            ballColor = "Blue"

        payment = float(bets[j.realized_bet][chosen.ball - 1])

        total = j.earnings_bonus + payment
        j.earnings_task2 = total
        current_earnings = j.earnings_task1 + total


        j.totalearnings = current_earnings
        session.add(j)
        session.commit()
        
        return render_template('results_for_ball.html', chosen = chosen, CorD = CorD, cr=cr, line=line, bonus = bonus, payment = payment, ballColor = ballColor, subject_id = subject_id, bets=bets, total = total, current_earnings = current_earnings, realized_bet=j.realized_bet)

####
#####
######
####### ADMIN Create page
######
#####
####



@app.route('/admin_create', methods=['POST'])
def AdminCreatePage():

        session_no = request.form['session_no']

        newchosen = ChosenOnes(session_no = session_no)
        session.add(newchosen)
        session.commit()

        chosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()

        if chosen.ball == 1:
            ballColor = "Green"
        elif chosen.ball == 2:
            ballColor = "Orange"
        else:
            ballColor = "none"

        return render_template('admin.html', chosen = chosen, ballColor=ballColor)

@app.route('/admin_update', methods=['POST'])
def AdminUpdatePage():

        session_no = request.form['session_no']

        #chages the new entieries, but only if something was entered in the form (does not make blank)

        newchosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()
        if request.form['rnd']:
            newchosen.rnd = request.form['rnd']
        if request.form['line']:
            newchosen.line = request.form['line']
        if request.form['word']:
            newchosen.word = request.form['word']
        if request.form['urn']:
            newchosen.urn = request.form['urn']
        if request.form['ball']:
            newchosen.ball = request.form['ball']
        session.add(newchosen)
        session.commit()

        newchosen2 = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()

        if newchosen2.rnd != None:
            wait_end_session_v = request.form['wait_end_session']
            if wait_end_session_v == "True":
                newchosen2.wait_end_session = True
                session.add(newchosen2)
                session.commit()
            elif wait_end_session_v == "False":
                newchosen2.wait_end_session = False
                session.add(newchosen2)
                session.commit()

        if newchosen2.wait_end_session == True and newchosen2.line != None and newchosen2.word != None and newchosen2.urn != None:
            wait_for_word_urn_v = request.form['wait_for_word_urn']
            if wait_for_word_urn_v == "True":
                newchosen2.wait_for_word_urn = True
                session.add(newchosen2)
                session.commit()
            elif wait_for_word_urn_v == "False":
                newchosen2.wait_for_word_urn = False
                session.add(newchosen2)
                session.commit()

        if newchosen2.wait_for_word_urn == True and newchosen2.ball != None:
        	wait_for_delay_entry_v = request.form['wait_for_delay_entry']
        	if wait_for_delay_entry_v == "True":
        		newchosen2.wait_for_delay_entry = True
        		session.add(newchosen2)
        		session.commit()
        	elif wait_for_delay_entry_v == "False":
        	    newchosen2.wait_for_delay_entry = False
        	    session.add(newchosen2)
        	    session.commit()

        wait_for_part_2_v = request.form['wait_for_part_2']
        if wait_for_part_2_v == "True":
            newchosen2.wait_for_part_2 = True
            session.add(newchosen2)
            session.commit()
        elif wait_end_session_v == "False":
            newchosen2.wait_for_part_2 = False
            session.add(newchosen2)
            session.commit()

        chosen = session.query(ChosenOnes).filter(ChosenOnes.session_no == session_no).order_by(ChosenOnes.id.desc()).first()


        if chosen.ball == 1:
            ballColor = "Yellow"
        elif chosen.ball == 2:
            ballColor = "Blue"
        else:
            ballColor = "none"

        if chosen.urn == 1:
            urnchoice = "Heads"
        elif chosen.urn == 2:
            urnchoice = "Tails"
        else:
            urnchoice = "none"


        return render_template('admin.html', chosen = chosen, ballColor=ballColor, urnchoice=urnchoice)


####
#####
######
####### Risk ELicitation
######
#####
####

@app.route('/risk_e', methods=['POST'])
def RiskElicit():

    subject_id=request.form['subject_id']
    state_update = request.form['gamble']

    j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
    old_state = j.risk_state

    j.risk_state = old_state + state_update
    session.add(j)
    session.commit()

    state = j.risk_state

    len_state = len(state) 

    gamble = session.query(DOSEGambles).filter(DOSEGambles.risk_state == state).one()

    if len(state) < 4:
        return render_template('risk_elicitation.html', subject_id=subject_id, state=state, len_state=len_state, gamble=gamble, v=True)
    else:
        return render_template('risk_elicitation.html', subject_id=subject_id, state=state, len_state=len_state, gamble=gamble, v=False)


@app.route('/risk_feedback', methods=['POST'])
def RiskFeedback():

    subject_id=request.form['subject_id']
    state_update = request.form['gamble']

    j = session.query(Subject).filter(Subject.subject_name == subject_id).one()
    old_state = j.risk_state

    j.risk_state = old_state + state_update
    session.add(j)
    session.commit()

    state = j.risk_state

    x = randint(1,4) #choose round to pay
    chosen_round = state[:x] #get gambles from that round
    gamble = session.query(DOSEGambles).filter(DOSEGambles.risk_state == chosen_round).one()

    y = state[x]
    z = randint(1,100) #choose random draw

    if y == "1":
        Threshold = gamble.gamble_1_h #gamble cutoff for random draw
        first = True
        risk_payment = 3.85
        if z > Threshold:
            risk_payment = .1

    if y == '2':
        Threshold = gamble.gamble_2_h
        first = False
        risk_payment = 2
        if z > Threshold:
            risk_payment = 1.6




    j.earnings_risk = risk_payment
    j.totalearnings = j.earnings_task1 + j.earnings_task2 + risk_payment

    session.add(j)
    session.commit()

    return render_template('risk_feedback.html', subject_id=subject_id, x=x, state=state, first=first, gamble=gamble, randdraw=z, risk_payment=risk_payment)


@app.route('/survey', methods=['POST'])
def Survey():

    subject_id=request.form['subject_id']

    return render_template('survey.html',  subject_id=subject_id)


@app.route('/final_payment', methods=['POST'])
def FinalPayment():

    subject_id=request.form['subject_id']
    s_age = request.form['age']
    s_gender = request.form['gender']
    s_ethnicity = request.form['race']
    s_move_to_us = request.form['us']
    s_lang = request.form['lang']
    s_degree = request.form['degree']
    s_year_in_school = request.form['year']
    s_major = request.form['major']
    s_exp_studies = request.form['exp']

    j = session.query(Subject).filter(Subject.subject_name == subject_id).one()

    j.s_age = s_age
    j.s_gender = s_gender
    j.s_ethnicity =s_ethnicity
    j.s_move_to_us=s_move_to_us
    j.s_lang=s_lang
    j.s_degree=s_degree
    j.s_year_in_school=s_year_in_school
    j.s_major=s_major
    j.s_exp_studies=s_exp_studies 

    session.add(j)
    session.commit()

    return render_template('final_payment.html',  subject_id=subject_id, j=j)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



