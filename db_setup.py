

# from flask_sqlalchemy import SQLAlchemy

import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import create_engine

Base = declarative_base()

class SubjectLetterBank(Base):
    __tablename__ = "subject_letter_bank"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    letter_bank_id = Column(Integer, ForeignKey("letter_bank.id"))
    rnd = Column(Integer)
    task = Column(Integer)
    subjects = relationship('Subject', back_populates="letters")
    letters = relationship('LetterBank', back_populates="subjects")

    def __init__(self, rnd, task):
        self.rnd = rnd
        self.task = task

class LetterBank(Base):
    __tablename__ = 'letter_bank'

    id = Column(Integer, primary_key=True)
    name = Column(String(6), nullable=False)
    letter0 = Column(String(1), nullable=False)
    letter1 = Column(String(1), nullable=False)
    letter2 = Column(String(1), nullable=False)
    letter3 = Column(String(1), nullable=False)
    letter4 = Column(String(1), nullable=False)
    letter5 = Column(String(1), nullable=False)
    subjects = relationship('SubjectLetterBank', back_populates="letters")

class BDMLines(Base):
    __tablename__ = 'bdm_lines'

    id = Column(Integer, primary_key=True)
    line_name = Column(String(10))
    line_number = Column(Integer)
    contract_bonus = Column(Integer)
    delay_bonus = Column(Integer)


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(5))
    treatment = Column(Integer, default=1)
    session_no = Column(Integer, default=1)
    letters = relationship('SubjectLetterBank', back_populates="subjects")
    wait_end_session = Column(Boolean, unique=False, default=True) #defult is true, becomes false at start, then true again when done with all entry
    wait_for_word_urn = Column(Boolean, unique=False, default=True) #after task1 payment, before task2 payment.
    wait_for_delay_entry = Column(Boolean, unique=False, default=True) #when done with entering bets if choose delay
    wait_r1 = Column(Boolean, unique=False, default=True)
    wait_for_part_2= Column(Boolean, unique=False, default=True)
    last_round_completed = Column(Integer, default=0)
    realized_bet = Column(String(5))
    earnings_task1 = Column(Integer, default=0)
    earnings_bonus = Column(Integer, default=0)
    earnings_task2 = Column(Integer, default=0)
    earnings_risk = Column(Integer, default=0)
    totalearnings = Column(Integer, default=0)
    risk_state = Column(String(10), default="0000")
    risk_choice1 = Column(String(10), default="0")
    risk_choice2 = Column(String(10), default="0")
    risk_choice3 = Column(String(10), default="0")
    risk_choice4 = Column(String(10), default="0")
    s_age = Column(Integer)
    s_gender = Column(String(50))
    s_ethnicity = Column(String(50))
    s_move_to_us = Column(String(50))
    s_lang = Column(String(50))
    s_degree = Column(String(50))
    s_year_in_school = Column(String(50))
    s_major = Column(String(50))
    s_exp_studies = Column(Integer)


class TimeStarted(Base):
    __tablename__ = 'time_started'
    id = Column(Integer, primary_key=True)
    rnd = Column(Integer)
    task = Column(Integer)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(Subject)

class DataBDM(Base):
    __tablename__ = 'data_bdm'
    id = Column(Integer, primary_key=True)
    rnd = Column(Integer)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(Subject)
    bdm_lines_id = Column(Integer, ForeignKey('bdm_lines.id'))
    bdm_lines = relationship(BDMLines)
    contract_or_delay = Column(String(1))


class Contracts(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    word = Column(String(6), nullable=False)
    bet1 = Column(String(1), nullable=False)
    bet2 = Column(String(1), nullable=False)
    subject = Column(String(10))
    current_round = Column(Integer)
    display = Column(Boolean, unique=False, default=True)
    valid = Column(Boolean)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    #words = Column(String(250), nullable=False)

class FoundWords(Base):
    __tablename__ = 'found_words'

    id = Column(Integer, primary_key=True)
    word = Column(String(6), nullable=False)
    subject = Column(String(10))
    valid = Column(Boolean)
    current_round =  Column(Integer)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    #words = Column(String(250), nullable=False)

class WordBank(Base):
    __tablename__ = 'word_bank'

    word = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    letter_bank_id = Column(Integer, ForeignKey('letter_bank.id'))
    letter_bank = relationship(LetterBank)


class ChosenOnes(Base):
    __tablename__ = 'choosen_ones'

    id = Column(Integer, primary_key=True)
    #treatment = Column(Integer, default=1)
    session_no = Column(Integer)
    rnd = Column(Integer)
    line = Column(Integer)
    word = Column(String(10))
    urn = Column(Integer)
    ball = Column(Integer)
    wait_end_session = Column(Boolean, default=False) # for DRAWING ROUND
    wait_for_delay_entry = Column(Boolean, default=False) #when done with entering bets if choose delay, FOR DRAWING BALLS
    wait_for_word_urn = Column(Boolean, default=False) #for FOR DRAWING WORDS/URNS
    wait_for_part_2 = Column(Boolean, default=False) #for FOR Reading instuctions


class DOSEGambles(Base):
    __tablename__ = 'dose_gambles'

    id = Column(Integer, primary_key=True)
    risk_state = Column(String(10))
    gamble_1_h = Column(Integer)
    gamble_2_h = Column(Integer)







filePath = os.getcwd()
engine = create_engine('sqlite:///'+ filePath + '/restaurantmenu.db')


Base.metadata.create_all(engine)

