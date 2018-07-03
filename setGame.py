#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:22:04 2017

@author: Felipe
"""

###############################################################################
###              UNAWARENESS EXPERIMENT: CODE FOR SET GAME                  ###
###############################################################################

import itertools, time, random, math
import pylab
import matplotlib.pyplot as plt

class Deck(object):
    """
    A class to represent a deck of cards with specific properties
    """
    def __init__(self, properties):
        """
        properties is a dictionary: keys are the names of the properties,
                values are lists with the possible instances of each property
        """
        self.properties = properties
    def getProperties(self):
        return self.properties
    def getNumCards(self):
        """
        Returns the total number of cards in the deck. This definition is 
            robust to decks that have properties with different number of
            instances
        """
        numCards = 1
        for key in self.properties:
            numCards *= len(self.properties[key])
        return numCards
        
# Functions to be used with objects from the Deck class:    
        
def getCards(deck):
    """
    'deck' is a Deck object.
    Return a list with every card of the deck, where each card is a tuple with
            the values of each one of the properties.
    This version ONLY works with decks with 2, 3, 4, or 5 properties. However, 
            the properties themselves can have an arbritrary number of 
            values (or instances).

            ##changed tuples to list becuase javascript needs sq brakets. really!
    """
    listKeys = []
    for key in deck.getProperties():
        listKeys.append(key)
    if len(deck.getProperties()) == 2:
        return list(list(tup) for tup in itertools.product(deck.getProperties()[listKeys[0]],
                                  deck.getProperties()[listKeys[1]])) 
    elif len(deck.getProperties()) == 3:
        return list(list(tup) for tup in itertools.product(deck.getProperties()[listKeys[0]],
                                  deck.getProperties()[listKeys[1]],
                                  deck.getProperties()[listKeys[2]]))    
    elif len(deck.getProperties()) == 4:
        return list(list(tup) for tup in itertools.product(deck.getProperties()[listKeys[0]],
                                  deck.getProperties()[listKeys[1]],
                                  deck.getProperties()[listKeys[2]],
                                  deck.getProperties()[listKeys[3]]))
    elif len(deck.getProperties()) == 5:
        return list(list(tup) for tup in itertools.product(deck.getProperties()[listKeys[0]],
                                  deck.getProperties()[listKeys[1]],
                                  deck.getProperties()[listKeys[2]],
                                  deck.getProperties()[listKeys[3]],
                                  deck.getProperties()[listKeys[4]]))
    
def isSetThreeCards(cards):
    """
    'cards' is a list (or tuple) with three cards, which are themselves tuples
    Returns: True if the cards form a set, False otherwise
    
    Recall that a set is formed whenever EACH of the properties is either
            the same in ALL cards or different in ALL cards
    
    WARNING: this function only makes sense when evaluating groups of THREE
            cards
    """
    result = True
    for i in range(len(cards[0])): #all cards have the same num of properties
        if ( cards[0][i] == cards[1][i] ) & ( cards[0][i] != cards[2][i] ):
            result = False
        elif ( cards[0][i] != cards[1][i] ) & ( cards[0][i] == cards[2][i] ):
            result = False
        elif ( cards[0][i] != cards[1][i] ) & ( cards[1][i] == cards[2][i] ):
            result = False
    return result
            
def cardCombinations(deck, n):
    """
    WARNING: think about how big the number is before using, for it might freeze 
            your computer
            
    deck: a Deck object
    n: number of cards in each group ( int > 0 )
    
    Returns a list of tuples of three cards representing ALL possible 
            combinations of n cards for that a particular deck. Recall that each
            card is itself a tuple with as many elements as there are keys in 
            the properties dictionary
    """
    return list(itertools.combinations(getCards(deck), n))
    
def totalNumSets(deck, n):
    """
    deck: a Deck object
    n: number of cards per set ( int > 0 )
    
    Returns the total number of sets of size n that can be formed with the 
            cards in the deck
            
    WARNING: will only work with n=3 as long as the function used is
            'isSetThreeCards'
    """
    start_time = time.time()
    listCombinations = cardCombinations(deck, n)
    count = 0
    for i in range(len(listCombinations)):
        if isSetThreeCards(listCombinations[i]):
            count += 1
    total_time = time.time() - start_time
    return count, total_time
    
def proportionSets(deck,n):
    """
    Returns the ratio of sets over all possible combinations of n cards
    """
    return totalNumSets(deck,n)[0] / len(cardCombinations(deck,n))
    
def validSets(deck, n):
    """
    deck: a Deck object
    n: number of cards per set ( int > 0 )
    
    Returns a list of tuples of cards that form valid sets
    """
    listCombinations = cardCombinations(deck, n)
    validSets = []
    for i in range(len(listCombinations)):
        if isSetThreeCards(listCombinations[i]):
            validSets.append(listCombinations[i])
    return validSets  

    
def makeHistSimulation(deck, handSize, trials, setSize):
    """
    deck: a Deck object
    handSize: number of cards from Deck to be dealt in a hand ( int > 0 )
    trials: number of simulations performed ( int > 0 )
    setSize: number of cards in each set (usually equal to 3)
    
    Returns: a histogram of total number of sets per subDeck (or hand)
    """
    random.seed(0)
    C = []
    sampleCards = []
    listTotal = []
    listCards = getCards(deck)
    repeated = 0
    usedSamples = []
    tupleValues = []
    ev = 0
    var = 0
    sd = 0
    for key in deck.getProperties():
        tupleValues.append(len(deck.getProperties()[key]))
    for trial in range(trials):
        count = 0
        total = 0
        sampleCards = random.sample(listCards, handSize)
        if sampleCards not in usedSamples:
            usedSamples.append(sampleCards)
            C = list(itertools.combinations(sampleCards, setSize))
            while count < len(C):
                if isSetThreeCards(C[count]):
                    total += 1
                count += 1
            listTotal.append(total)
        elif sampleCards in usedSamples:
            repeated += 1
    numSets = []
    numHands = []
    for i in range(max(listTotal)+1):
        numSets.append(i)
    for n in range(len(numSets)):
        count = 0
        for i in range(len(listTotal)):
            if numSets[n]==listTotal[i]:
                count+=1
        numHands.append(count)
    # Get expected value and standard deviation
    for i in range(len(numSets)):
        ev += ( numSets[i]*numHands[i] ) / sum(numHands)
    for i in range(len(numSets)):
        var += ( ( numSets[i] - ev ) ** 2 ) * ( numHands[i] / sum(numHands) )
    sd = math.sqrt(var)
    pylab.bar(numSets, numHands, align='center')
    pylab.xlim([0,max(numSets)+1])
    pylab.title('Size of deck: ' + str(deck.getNumCards()) + ' | Properties: ' 
                + str(tupleValues) + '\n' + 'Trials: ' + str(trials) 
                + ' | Cards per hand: ' + str(handSize) + ' | SET size: ' 
                + str(setSize))
    pylab.xlabel('Max. number of SETS')
    pylab.ylabel('Unique hands of size ' + str(handSize))
    plt.savefig(str(deck.getNumCards())+'Deck_'+str(handSize)+'Cards_'
                +str(setSize)+'-cardSet'+'.pdf')
    pylab.close()
    return numSets, numHands, (ev, var, sd)

def getSetsSimulation(deck, handSize, trials, setSize, randomSeed):
    """
    deck: a Deck object
    handSize: number of cards from Deck to be used ( int > 0 )
    trials: number of simulations performed ( int > 0 )
    setSize: number of cards in each set, usually equal to 3
    randomSeed: seed to be used for the random components
    
    Returns: a dictionary with every combination of cards and sets formed with 
            those cards. Each key represents the number of possible sets, 
            starting from the minimum number of sets. Associated
            with each key is a list with as many elements as there are
            sampleCards with that number 'key' of possible sets.  
            Each element is itself a list with two elements: the first is a 
            tuple with the exact subDeck of handSize-cards. The second 
            element is a list with all possible sets of size setSize that was 
            formed with those sampleSize-cards (the total number of sets is, of
            course, equal to the 'key')
    """
    random.seed(randomSeed)
    C = []
    sampleCards = []
    listTotal = []
    listCards = getCards(deck)
    repeated = 0
    usedSamples = []
    finalResult = {}
    for trial in range(trials):
        tempSet = [] #temporarily add sets before associating with KEY
        count = 0
        total = 0
        sampleCards = random.sample(listCards, handSize)
        if sampleCards not in usedSamples:
            usedSamples.append(sampleCards)
            C = list(itertools.combinations(sampleCards, setSize))
            while count < len(C):
                if isSetThreeCards(C[count]):
                    total += 1
                    tempSet.append(C[count])
                count += 1
        elif sampleCards in usedSamples:
            repeated += 1
        if total not in finalResult:
            finalResult[total] = [[sampleCards,tempSet]]
        elif total in finalResult:
            finalResult[total].append([sampleCards, tempSet])
        listTotal.append(total)
    return finalResult

def getNhands(deck, handSize, trials):
    """
    deck: a Deck object
    handSize: number of cards from Deck to be used ( int > 0 )
    trials: number of simulations performed ( int > 0 )
    setSize: number of cards in each set, usually equal to 3
    randomSeed: seed to be used for the random components
    
    Returns: a dictionary with every combination of cards and sets formed with 
            those cards. Each key represents the number of possible sets, 
            starting from the minimum number of sets. Associated
            with each key is a list with as many elements as there are
            sampleCards with that number 'key' of possible sets.  
            Each element is itself a list with two elements: the first is a 
            tuple with the exact subDeck of handSize-cards. The second 
            element is a list with all possible sets of size setSize that was 
            formed with those sampleSize-cards (the total number of sets is, of
            course, equal to the 'key')
    """
    #random.seed(randomSeed)
    sampleCards = []
    listCards = getCards(deck)
    usedSamples = []
    finalResult = []
    for trial in range(trials):
        sampleCards = random.sample(listCards, handSize)
        if sampleCards not in usedSamples:
            finalResult.append(sampleCards)
    return finalResult

def getSubdeckNsets(deck, handSize, trials, setSize, nSets, randomSeed, nExamples):
    """
    deck: a Deck object
    handSize: number of cards from Deck to be used ( int > 0 )
    trials: number of simulations performed ( int > 0 )
    setSize: number of cards in each set, usually equal to 3
    nsets: number of sets desired (int > 0)
    randomSeed: seed to be used for the random components
    
    Returns: from 'finalResult' dictionary (see 'getSetsSimulation') randomly 
            picks 'nExamples' setSize-subDeck that generates 'nSets' number of sets. 
            If 'nExamples'is 1, returns a list of two lists: the first is a 
            list with the cards from the 'setSize-subDeck' and the second is a 
            list of tuples with all the 'nsets' number of sets formed by the 
            subDeck; if 'nExamples' is larger than 1, returns a 
            list-of-lists-of-lists.  
    """
    finalList = []
    dic = getSetsSimulation(deck, handSize, trials, setSize, randomSeed)
    if nExamples == 1:
        x = random.choice(range(len(dic[nSets])))
        finalList.append(dic[nSets][x][0])
        finalList.append(dic[nSets][x][1])
    else:
        x = random.sample(range(len(dic[nSets])),nExamples)
        for i in x:
            finalList.append([dic[nSets][i][0],dic[nSets][i][1]])
    return finalList
    
###############################################################################
###              SIMULATION: ORIGINAL AND THREEPROPERTIES DECKS             ###
###############################################################################

original = Deck({'number':[1,2,3],'symbol':['diamond', 'squiggle', 'oval'], 
        'shading':['solid', 'striped', 'open'], 'color':['red','green','purple']})

threeProperties = Deck({'number':[0,1,2,3],'color':[0,1,2,3]
                  ,'shape':[0,1,2,3]})

#listOfDecks = [original,threeProperties]
#
#listOfHands = [9,10,11,12]
#
#for deck in listOfDecks:
#    for handSize in listOfHands:
#        makeHistSimulation(deck, handSize, 50000, 3)

###############################################################################
###              RANDOMLY GENERATE HIGH- AND LOW-COUNT SUBDECKS             ###
###                       FOR TESTING IN THE VIZ PAGE                       ###    
###############################################################################

# Create a list with 5 decks of 10 sets each and one with 5 decks of 28 sets;
# first tests used random seed 0    
    
low_list = getSubdeckNsets(threeProperties,12,50000,3,10,1987,5)

high_list = getSubdeckNsets(threeProperties,12,50000,3,28,1987,5)