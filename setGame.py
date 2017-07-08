#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:22:04 2017

@author: Felipe
"""

###############################################################################
###              UNAWARENESS EXPERIMENT: CODE FOR SET GAME                  ###
###############################################################################

import itertools, time, pylab, random
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
    Return a list with every card of the deck, where each card is a tuple with
            the values of each one of the properties.
    This version ONLY works with decks with 2, 3, 4, or 5 properties. However, 
            the properties themselves can have an arbritrary number of 
            values (or instances)
    """
    listKeys = []
    for key in deck.getProperties():
        listKeys.append(key)
    if len(deck.getProperties()) == 2:
        return list(itertools.product(deck.getProperties()[listKeys[0]],
                                  deck.getProperties()[listKeys[1]])) 
    elif len(deck.getProperties()) == 3:
        return list(itertools.product(deck.getProperties()[listKeys[0]],
                                  deck.getProperties()[listKeys[1]],
                                  deck.getProperties()[listKeys[2]]))    
    elif len(deck.getProperties()) == 4:
        return list(itertools.product(deck.getProperties()[listKeys[0]],
                                  deck.getProperties()[listKeys[1]],
                                  deck.getProperties()[listKeys[2]],
                                  deck.getProperties()[listKeys[3]]))
    elif len(deck.getProperties()) == 5:
        return list(itertools.product(deck.getProperties()[listKeys[0]],
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
            combinations of n cards for that a prtciular deck. Recall that each
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
    return numSets, numHands

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

    
###############################################################################
###              SIMULATION: ORIGINAL AND THREEPROPERTIES DECKS             ###
###############################################################################

original = Deck({'number':[1,2,3],'symbol':['diamond', 'squiggle', 'oval'], 
        'shading':['solid', 'striped', 'open'], 'color':['red','green','purple']})

threeProperties = Deck({'number':[1,2,3,4],'color':['cyan','magenta','yellow','red']
                   ,'shape':['square','triangle','circle','squiggle']})

listOfDecks = [original,threeProperties]

listOfHands = [9,10,11,12]

#for deck in listOfDecks:
#    for handSize in listOfHands:
#        makeHistSimulation(deck, handSize, 20000, 3)

###############################################################################
###                   EXAMPLES TO BE USED WITH EXPERIMENT                   ###
###############################################################################

# We want to choose a subDeck of 10 cards, with a low number of possible sets

# The function 'getSetsSimulation' generates a dictionary where each is the 
#   number of sets that could be formed, and the values are lists of subDekcs
#   and sets formed with each subDeck. For example, say I want a subDeck that 
#   has 7 sets. Let's call the function with the key equal to 7:
    
#print(getSetsSimulation(threeProperties, 10, 10000, 3, 12345)[7])

# There is a lot here, because there are a lot of subDekcs that generate
#   exactly 7 sets. Let's compute exactly how many there are:
    
#print(len(getSetsSimulation(threeProperties, 10, 10000, 3, 12345)[7]))

# For this particular number of trials and random seed, there are 735 (unique) 
#   such subDecks. If you want to recover a particular subDeck, simply call
#   the function and recover the element of the list you're interested in. For
#   example, if you call the first element of function with the key 7, you'll
#   get a list of lists: the first element is the particular subDeck and the 
#   second is a list of all possible (7) sets formed with such cards:
    
#print(getSetsSimulation(threeProperties, 10, 10000, 3, 12345)[7][0])

# Then, if you call the first element of that, you'll get the subDeck of 10
#   card used to generate the sets:

#print(getSetsSimulation(threeProperties, 10, 10000, 3, 12345)[7][0][0])

# And you can use this element to generate the images for the experiment. Also, 
#   if you call the second element of that list of lists, you'll get all the 
#   possible sets formed with those cards:

#print(getSetsSimulation(threeProperties, 10, 10000, 3, 12345)[7][0][1])

# Which is, of course, a list of length 7, where each element is a tuple with
#   thee cards that form a seet. And you can go through this list to both 
#   generate images for the experiment and to check people's answers. 

