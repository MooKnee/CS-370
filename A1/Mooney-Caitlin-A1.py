import fileinput
import sys
from queue import *
'''
Name: Caitlin Mooney
Class: CS 370
Assignment: Assignment 1'''

def process_nodes():


# Inputs
f = open("nameOfFile.txt", 'r')
lines = f.readlines()
f.close()
queue = []
for line in range(len(lines)):
    queue.append(lines[line].strip())
# max size of queue
firstLine = int(queue[0])
# max total num of states
secondLine = int(queue[1])
# either 0 or 1
thirdLine = int(queue[2])
# number of dominoes
fourthLine = queue[3]
#start of dominoes
fifthLine = queue[4:]
dominoes = {}
for sets in range(len(fifthLine)):
  for lineSets in range(len(fifthLine)):
      getString = fifthLine[sets].split()
      dominoes[getString[0]] = [str(getString[1]),str(getString[2])]
  lineSet = f.readline()
  # domNum='D'+str(lines+1)
  # top=line.split(" ")[1]
  # bottom=line.split(" ")[2]
  # dominoes.append([domNum,top,bottom])
  dominoes.append(['D'+str(lines+1), line.split(" ")[1], line.split(" ")[2]])


def bfs(doms, maxSz):
    # queueDoms = Queue(maxsize = maxSz)
    # domNum=doms[0]
    # top=doms[1]
    # bottom=doms[2]
    queueDoms = []
    validStates = {}
    getSol = True
    depth = 1

    # check if each domino is valid and if can be shortend
    for domino in doms:
        dominoNum = domino[0]
        dominoTop = domino[1]
        dominoBot = domino[2]
        # if top is bigger than bottom
        if len(dominoTop) > len(dominoBot):
            # then check if bottom is in first part of top
            if dominoBot == dominoTop[:len(dominoBot)]:
                # then add to validStates and cut off top
                dominoTop = dominoTop[len(dominoBot):]
                dominoBot = ""
                validStates[dominoTop + ":"] = dominoNum
                queueDoms.append(domino)
        # if top is smaller than bottom
        if len(dominoTop) < len(dominoBot):
            # then check if top is in first part of bottom
            if dominoTop == dominoBot[:len(dominoTop)]:
                # then add to validStates and cut off bot
                dominoBot = dominoBot[:len(dominoTop)]
                dominoTop = ""
                validStates[":"+dominoBot] = dominoNum
                queueDoms.append(domino)
    while getSol == True and len(queueDoms) < maxSz:
        print("depth: "+str(depth+1))
        i = queueDoms.pop(0)
        iNum = i[0]
        iTop = i[1]
        iBot = i[2]
        currentDoms=[]
        #for stateVal in queueDoms[depth]:
        for dominoD in doms:
            dominoDNum = dominoD[0]
            dominoDTop = dominoD[1]
            dominoDBot = dominoD[2]
            newDom = [iNum+dominoDNum, iTop+dominoDTop, iBot+dominoDBot]
            newDom[0].append(dominoD[0])
            nDN = newDom[0]
            nDT = newDom[1]
            nDB = newDom[2]
            # if top is bigger than bottom
            if len(nDT) > len(nDB):
                # then check if bottom is in first part of top
                if nDB == nDT[:len(nDB)]:
                    currentDoms.append(newDom)
                    # then add to validStates and cut off top
                    nDT = nDT[len(nDB):]
                    nDB = ""
                    if nDT == nDB:
                        validStates[nDT + ":"] = nDN
                        #queueDoms.append(newDom)
                        getSol=False
            # if top is smaller than bottom
            if len(nDT) < len(nDB):
                # then check if top is in first part of bottom
                if nDT == nDB[:len(nDT)]:
                    currentDoms.append(newDom)
                    # then add to validStates and cut off bot
                    nDB = nDB[:len(nDT)]
                    nDT = ""
                    if nDT==nDB:
                        validStates[":"+nDB] = nDN
                        #queueDoms.append(newDom)
                        getSol=False
        queueDoms.append(currentDoms)
        depth+=1
        

  

print(bfs(dominoes,firstLine))


