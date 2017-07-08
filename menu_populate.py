

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import os

import db_setup

from db_setup import Base, engine, LetterBank, FoundWords, Subject, WordBank, Contracts, SubjectLetterBank, BDMLines, ChosenOnes, DOSEGambles
 
filePath = os.getcwd()
os.remove(filePath + '/restaurantmenu.db')
db_setup.Base.metadata.create_all(engine)


#engine = create_engine('sqlite:////Users/evanpiermont/Desktop/scrabble/restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#letters1
letters1Stage = 'dseotl'

letters1 = LetterBank(
    name = letters1Stage,
    letter0 = letters1Stage[0],
    letter1 = letters1Stage[1],
    letter2 = letters1Stage[2],
    letter3 = letters1Stage[3],
    letter4 = letters1Stage[4],
    letter5 = letters1Stage[5])


session.add(letters1)
session.commit()

#words

words1 = ['oldest','stole','soled','lodes','dotes','dolts','doles','doest','told','toes','toed','sole','sold','slot','sloe','sled','odes','lots','lost','lose','lode','lets','lest','dots','dote','dose','dolt','dole','does','toe','sot','sol','sod','set','old','ode','lot','let','led','els','dot','dos','doe']

for i in words1:
    wordsB1 = WordBank(word = i, letter_bank = letters1)
    session.add(wordsB1)
    session.commit()


#letters2
letters2Stage = 'aotnum'

letters2 = LetterBank(
    name = letters2Stage,
    letter0 = letters2Stage[0],
    letter1 = letters2Stage[1],
    letter2 = letters2Stage[2],
    letter3 = letters2Stage[3],
    letter4 = letters2Stage[4],
    letter5 = letters2Stage[5])


session.add(letters2)
session.commit()

#words

words2 = ['amount','mount','unto','tuna','naut','muon','moat','moan','auto','aunt','atom','ton','tau','tan','tam','out','oat','nut','not','mat','man','ant']

for i in words2:
    wordsB2 = WordBank(word = i, letter_bank = letters2)
    session.add(wordsB2)
    session.commit()

#letters3
letters3Stage = 'nigdes'

letters3 = LetterBank(
    name = letters3Stage,
    letter0 = letters3Stage[0],
    letter1 = letters3Stage[1],
    letter2 = letters3Stage[2],
    letter3 = letters3Stage[3],
    letter4 = letters3Stage[4],
    letter5 = letters3Stage[5])


session.add(letters3)
session.commit()

#words

words3 =['singed','signed','design','snide','singe','dings','dines','deign','sing','sine','sign','side','send','ides','gins','ends','dins','ding','dine','digs','dies','dens','sin','ins','ids','ide','gin','ens','end','din','dig','die','den'] 
for i in words3:
    wordsB3 = WordBank(word = i, letter_bank = letters3)
    session.add(wordsB3)
    session.commit()



#letters4
letters4Stage = 'teluma'

letters4 = LetterBank(
    name = letters4Stage,
    letter0 = letters4Stage[0],
    letter1 = letters4Stage[1],
    letter2 = letters4Stage[2],
    letter3 = letters4Stage[3],
    letter4 = letters4Stage[4],
    letter5 = letters4Stage[5])


session.add(letters4)
session.commit()


words4 =['amulet','metal','team','teal','tame','tale','mute','mule','melt','meat','meal','maul','mate','malt','male','lute','late','lame','alum','tea','tau','tam','met','mat','leu','let','lea','lam','eta','emu','elm','eat','ate','ale'] 
for i in words4:
    wordsB4 = WordBank(word = i, letter_bank = letters4)
    session.add(wordsB4)
    session.commit()


#letters5
letters5Stage = 'dnaeps'

letters5 = LetterBank(
    name = letters5Stage,
    letter0 = letters5Stage[0],
    letter1 = letters5Stage[1],
    letter2 = letters5Stage[2],
    letter3 = letters5Stage[3],
    letter4 = letters5Stage[4],
    letter5 = letters5Stage[5])


session.add(letters5)
session.commit()


words5 =['ads','and','ands','ape','aped','apes','asp','aspen','dean','deans','den','dens','end','ends','ens','nap','nape','napes','naps','neap','neaps','pad','pads','pan','pane','paned','panes','pans','pea','peas','pen','pend','pends','pens','sad','sand','sane','sap','sea','sedan','send','snap','spa','spade','span','sped','spend'] 
for i in words5:
    wordsB5 = WordBank(word = i, letter_bank = letters5)
    session.add(wordsB5)
    session.commit()

#letters6
letters6Stage = 'obasfe'

letters6 = LetterBank(
    name = letters6Stage,
    letter0 = letters6Stage[0],
    letter1 = letters6Stage[1],
    letter2 = letters6Stage[2],
    letter3 = letters6Stage[3],
    letter4 = letters6Stage[4],
    letter5 = letters6Stage[5])


session.add(letters6)
session.commit()


words6 =['sofa','safe','oafs','foes','fobs','boas','base','sob','sea','oaf','foe','boa','abs'] 
for i in words6:
    wordsB6 = WordBank(word = i, letter_bank = letters6)
    session.add(wordsB6)
    session.commit()

#letters7
letters7Stage = 'ebtoan'

letters7 = LetterBank(
    name = letters7Stage,
    letter0 = letters7Stage[0],
    letter1 = letters7Stage[1],
    letter2 = letters7Stage[2],
    letter3 = letters7Stage[3],
    letter4 = letters7Stage[4],
    letter5 = letters7Stage[5])


session.add(letters7)
session.commit()

words7 =['baton','atone','tone','note','neat','bone','boat','beta','bent','beat','bean','bane','ante','abet','ton','toe','ten','tea','tan','tab','one','oat','not','nob','net','nab','eta','eon','eat','boa','bet','bat','ban','ate','ant'] 
for i in words7:
    wordsB7 = WordBank(word = i, letter_bank = letters7)
    session.add(wordsB7)
    session.commit()


#letters8
letters8Stage = 'acgofr'

letters8 = LetterBank(
    name = letters8Stage,
    letter0 = letters8Stage[0],
    letter1 = letters8Stage[1],
    letter2 = letters8Stage[2],
    letter3 = letters8Stage[3],
    letter4 = letters8Stage[4],
    letter5 = letters8Stage[5])


session.add(letters8)
session.commit()


words8 =['cargo','orca','frog','fora','crag','afro','rag','oar','oaf','fro','for','fog','far','cog','car','arc','ago'] 
for i in words8:
    wordsB8 = WordBank(word = i, letter_bank = letters8)
    session.add(wordsB8)
    session.commit()


#letters9
letters9Stage = 'marfde'


letters9 = LetterBank(
    name = letters9Stage,
    letter0 = letters9Stage[0],
    letter1 = letters9Stage[1],
    letter2 = letters9Stage[2],
    letter3 = letters9Stage[3],
    letter4 = letters9Stage[4],
    letter5 = letters9Stage[5])


session.add(letters9)
session.commit()


words9 =['framed','farmed','frame','fared','famed','dream','derma','armed','ream','read','mead','mare','made','fear','farm','fare','fame','fade','dram','derm','dear','deaf','dare','dame','ref','red','ram','mar','mad','fed','far','fad','era','ear','dam','arm','are'] 
for i in words9:
    wordsB9 = WordBank(word = i, letter_bank = letters9)
    session.add(wordsB9)
    session.commit()


#letters10
letters10Stage = 'ritelf'


letters10 = LetterBank(
    name = letters10Stage,
    letter0 = letters10Stage[0],
    letter1 = letters10Stage[1],
    letter2 = letters10Stage[2],
    letter3 = letters10Stage[3],
    letter4 = letters10Stage[4],
    letter5 = letters10Stage[5])


session.add(letters10)
session.commit()


words10 =['trifle','lifter','filter','tiler','rifle','relit','refit','litre','liter','lifer','flirt','flier','filet','filer','tire','tile','tier','rite','rile','rift','rife','riel','lite','lire','lift','life','lier','left','fret','flit','fire','file','felt','tie','ref','lit','lie','let','ire','fit','fir','elf'] 
for i in words10:
    wordsB10 = WordBank(word = i, letter_bank = letters10)
    session.add(wordsB10)
    session.commit()

#letters11
letters11Stage = 'axndte'


letters11 = LetterBank(
    name = letters11Stage,
    letter0 = letters11Stage[0],
    letter1 = letters11Stage[1],
    letter2 = letters11Stage[2],
    letter3 = letters11Stage[3],
    letter4 = letters11Stage[4],
    letter5 = letters11Stage[5])


session.add(letters11)
session.commit()


words11 =['taxed','tend','next','neat','dent','dean','date','axed','ante','ten','tea','tax','tan','tad','net','eta','end','eat','den','axe','ate','ant','and'] 
for i in words11:
    wordsB11 = WordBank(word = i, letter_bank = letters11)
    session.add(wordsB11)
    session.commit()

#letters12
letters12Stage = 'srteof'


letters12 = LetterBank(
    name = letters12Stage,
    letter0 = letters12Stage[0],
    letter1 = letters12Stage[1],
    letter2 = letters12Stage[2],
    letter3 = letters12Stage[3],
    letter4 = letters12Stage[4],
    letter5 = letters12Stage[5])


session.add(letters12)
session.commit()


words12 =['softer','foster','fortes','forest','store','frost','frets','forts','forte','tore','toes','sort','sore','soft','serf','rots','rote','rose','roes','rest','refs','ores','fret','fort','fore','foes','eros','toe','sot','set','rot','roe','ref','ors','ore','oft','fro','for','foe','efs'] 
for i in words12:
    wordsB12 = WordBank(word = i, letter_bank = letters12)
    session.add(wordsB12)
    session.commit()


#letters13
letters13Stage = 'veocal'


letters13 = LetterBank(
    name = letters13Stage,
    letter0 = letters13Stage[0],
    letter1 = letters13Stage[1],
    letter2 = letters13Stage[2],
    letter3 = letters13Stage[3],
    letter4 = letters13Stage[4],
    letter5 = letters13Stage[5])


session.add(letters13)
session.commit()


words13 =['alcove','vocal','clove','clave','calve','vole','vela','veal','vale','oval','love','lave','lace','cove','cole','cola','coal','cave','aloe','ova','lev','lea','ale','ace'] 
for i in words13:
    wordsB13 = WordBank(word = i, letter_bank = letters13)
    session.add(wordsB13)
    session.commit()

#letters14
letters14Stage = 'rveain'


letters14 = LetterBank(
    name = letters14Stage,
    letter0 = letters14Stage[0],
    letter1 = letters14Stage[1],
    letter2 = letters14Stage[2],
    letter3 = letters14Stage[3],
    letter4 = letters14Stage[4],
    letter5 = letters14Stage[5])


session.add(letters14)
session.commit()


words14 =['vainer','ravine','naiver','riven','raven','naive','vine','vein','vear','vane','vain','rive','rein','rave','rain','nevi','near','nave','earn','aver','vie','via','van','rev','ran','ire','era','ear','are','air'] 
for i in words14:
    wordsB14 = WordBank(word = i, letter_bank = letters14)
    session.add(wordsB14)
    session.commit()


# enter BDM lines

line1 = BDMLines(line_number = 1, line_name="line1", contract_bonus = 0, delay_bonus = 7)
line2 = BDMLines(line_number = 2, line_name="line2", contract_bonus = 0, delay_bonus = 6)
line3 = BDMLines(line_number = 3, line_name="line3", contract_bonus = 0, delay_bonus = 5)
line4 = BDMLines(line_number = 4, line_name="line4", contract_bonus = 0, delay_bonus = 4)
line5 = BDMLines(line_number = 5, line_name="line5", contract_bonus = 0, delay_bonus = 3)
line6 = BDMLines(line_number = 6, line_name="line6", contract_bonus = 0, delay_bonus = 2)
line7 = BDMLines(line_number = 7, line_name="line7", contract_bonus = 0, delay_bonus = 1)
line8 = BDMLines(line_number = 8, line_name="line8", contract_bonus = 0, delay_bonus = 0)
line9 = BDMLines(line_number = 9, line_name="line9", contract_bonus = 1, delay_bonus = 0)
line10 = BDMLines(line_number = 10, line_name="line10", contract_bonus = 2, delay_bonus = 0)
line11 = BDMLines(line_number = 11, line_name="line11", contract_bonus = 3, delay_bonus = 0)
line12 = BDMLines(line_number = 12, line_name="line12", contract_bonus = 4, delay_bonus = 0)
line13 = BDMLines(line_number = 13, line_name="line13", contract_bonus = 5, delay_bonus = 0)
line14 = BDMLines(line_number = 14, line_name="line14", contract_bonus = 6, delay_bonus = 0)
line15 = BDMLines(line_number = 15, line_name="line15", contract_bonus = 7, delay_bonus = 0)



session.add(line1)
session.add(line2)
session.add(line3)
session.add(line4)
session.add(line5)
session.add(line6)
session.add(line7)
session.add(line8)
session.add(line9)
session.add(line10)
session.add(line11)
session.add(line12)
session.add(line13)
session.add(line14)
session.add(line15)

session.commit()


#enter users
user1 = Subject(subject_name = '01usr1f', session_no = 1, treatment = 1)

session.add(user1)
session.commit()


user2 = Subject(subject_name = '01usr2g', session_no = 1, treatment = 2)

session.add(user2)
session.commit()


user3 = Subject(subject_name = '01usr3h', session_no = 1, treatment = 1)

session.add(user3)
session.commit()

user4 = Subject(subject_name = '01usr4i', session_no = 1, treatment = 2)

session.add(user4)
session.commit()


user5 = Subject(subject_name = '01usr5j', session_no = 1, treatment = 1)

session.add(user5)
session.commit()


user6 = Subject(subject_name = '01usr6k', session_no = 1, treatment = 2)

session.add(user6)
session.commit()

user7 = Subject(subject_name = '01usr7l', session_no = 1, treatment = 1)

session.add(user7)
session.commit()


user8 = Subject(subject_name = '01usr8m', session_no = 1, treatment = 2)

session.add(user8)
session.commit()


user9 = Subject(subject_name = '01usr9n', session_no = 1, treatment = 1)

session.add(user9)
session.commit()

user10 = Subject(subject_name = '01usr10o', session_no = 1, treatment = 2)

session.add(user10)
session.commit()

user11 = Subject(subject_name = '01usr11p', session_no = 1, treatment = 1)

session.add(user11)
session.commit()

user12 = Subject(subject_name = '01usr12q', session_no = 1, treatment = 2)

session.add(user12)
session.commit()

user13 = Subject(subject_name = '01usr13r', session_no = 1, treatment = 1)

session.add(user13)
session.commit()


users = session.query(Subject).all()

for user in users:
    a = SubjectLetterBank(rnd=1, task=1)
    q = session.query(LetterBank).get(1)
    a.letters = q
    user.letters.append(a)
    
    b = SubjectLetterBank(rnd=1, task=2)
    q = session.query(LetterBank).get(2)
    b.letters = q
    user.letters.append(b)
    
    c = SubjectLetterBank(rnd=2, task=1)
    q = session.query(LetterBank).get(3)
    c.letters = q
    user.letters.append(c)
    
    d = SubjectLetterBank(rnd=2, task=2)
    q = session.query(LetterBank).get(4)
    d.letters = q
    user.letters.append(d)

    e = SubjectLetterBank(rnd=3, task=1)
    q = session.query(LetterBank).get(5)
    e.letters = q
    user.letters.append(e)
    
    f = SubjectLetterBank(rnd=3, task=2)
    q = session.query(LetterBank).get(6)
    f.letters = q
    user.letters.append(f)

    g = SubjectLetterBank(rnd=4, task=1)
    q = session.query(LetterBank).get(7)
    g.letters = q
    user.letters.append(g)
    
    h = SubjectLetterBank(rnd=4, task=2)
    q = session.query(LetterBank).get(8)
    h.letters = q
    user.letters.append(h)
    
    i = SubjectLetterBank(rnd=5, task=1)
    q = session.query(LetterBank).get(9)
    i.letters = q
    user.letters.append(i)
    
    j = SubjectLetterBank(rnd=5, task=2)
    q = session.query(LetterBank).get(10)
    j.letters = q
    user.letters.append(j)

    k = SubjectLetterBank(rnd=6, task=1)
    q = session.query(LetterBank).get(11)
    k.letters = q
    user.letters.append(k)
    
    l = SubjectLetterBank(rnd=6, task=2)
    q = session.query(LetterBank).get(12)
    l.letters = q
    user.letters.append(l)

    m = SubjectLetterBank(rnd=7, task=1)
    q = session.query(LetterBank).get(13)
    m.letters = q
    user.letters.append(m)
    
    n = SubjectLetterBank(rnd=7, task=2)
    q = session.query(LetterBank).get(14)
    n.letters = q
    user.letters.append(n)

    session.add(user)
    session.commit()





#
# enter dose gambles
#

gamble0 = DOSEGambles(risk_state = '0000', gamble_1_h = 65, gamble_2_h = 65)

gamble01 = DOSEGambles(risk_state = '1000', gamble_1_h = 52, gamble_2_h = 52)
gamble02 = DOSEGambles(risk_state = '2000', gamble_1_h = 88, gamble_2_h = 88)

gamble011 = DOSEGambles(risk_state = '1100', gamble_1_h = 16, gamble_2_h = 16)
gamble021 = DOSEGambles(risk_state = '2100', gamble_1_h = 73, gamble_2_h = 73)
gamble012 = DOSEGambles(risk_state = '1200', gamble_1_h = 58, gamble_2_h = 58)
gamble022 = DOSEGambles(risk_state = '2200', gamble_1_h = 87, gamble_2_h = 87)

gamble0111 = DOSEGambles(risk_state = '1110', gamble_1_h = 14, gamble_2_h = 14)
gamble0211 = DOSEGambles(risk_state = '2110', gamble_1_h = 68, gamble_2_h = 68)
gamble0121 = DOSEGambles(risk_state = '1210', gamble_1_h = 59, gamble_2_h = 59)
gamble0221 = DOSEGambles(risk_state = '2210', gamble_1_h = 0, gamble_2_h = 0) 
gamble0112 = DOSEGambles(risk_state = '1120', gamble_1_h = 47, gamble_2_h = 47)
gamble0212 = DOSEGambles(risk_state = '2120', gamble_1_h = 92, gamble_2_h = 92)
gamble0122 = DOSEGambles(risk_state = '1220', gamble_1_h = 52, gamble_2_h = 52)
gamble0222 = DOSEGambles(risk_state = '2220', gamble_1_h = 91, gamble_2_h = 91)

session.add(gamble0)
session.add(gamble01)
session.add(gamble02)
session.add(gamble011)
session.add(gamble021)
session.add(gamble012)
session.add(gamble022)
session.add(gamble0111)
session.add(gamble0211)
session.add(gamble0121)
session.add(gamble0221)
session.add(gamble0112)
session.add(gamble0212)
session.add(gamble0122)
session.add(gamble0222)
session.commit()

print "added stuff!"


