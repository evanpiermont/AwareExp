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

@app.route('/', methods=['POST, GET'])
def CreateSets():

 
        subject_id=request.form['subject_id']

        sub = session.query(Subject).all()
        subjectnames = []
        for i in sub:
           subjectnames.append(i.idCode)

        #get list of valid subject names, next we test the input name to
        #sure the imput is valid

        if subject_id in subjectnames:

            j = session.query(Subject).filter(Subject.idCode == subject_id).one()        
            return render_template('set.html', subject_id = subject_id)

        else:
            return render_template('login.html', v=False)




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



