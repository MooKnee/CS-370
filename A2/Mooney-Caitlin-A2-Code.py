
#Name: Caitlin Mooney
#Class: CS 370 451
#Assignment: Assignment 2 Programming

# Atom: is denoted by a natural number: 1, 2, 3; 1 is literal P and -1 is literal !=P
# Clause: is line of text containing integers of corresponding literals
# after all clauses are given, next line is just 0, and everything after is ignored

# First, list of pairs of atoms (natural number) and truth value (T or F)
# Second, line containing only 0
# Third, remaining lines after 0 in input file is reproduced exactly
# max 1000 atoms
# max 10,000 clauses

#ATOMS = {}
#S = {}
def DP(ATOMS, S):
  V = {}
  for ATOM in ATOMS:
    V[ATOM] = None
  return DPHelper(ATOMS, S, V)

def DPHelper(ATOMS, S, V):
  if S is None or len(S)==0:
    #assign all remaing unbound atoms T or F arbitrarily
    return V
  if None in S:
    return None
  
  hasSetAtom = False
  for AtomKey in ATOMS:
    atom = ATOMS[AtomKey]
    if V[AtomKey] == None:
      if atom[0]==0 or atom[1]==0:
        V[AtomKey] = atom[1]==0
        hasSetAtom = True
    
  for clause in S:
    if len(clause)==1:
      key = abs(clause[0])
      if V[key]==None:
        V[key] = clause[0] > 0
        hasSetAtom = True

  #situation in which there is no set atom
  if not hasSetAtom:
    for settingAtoms in V:
      if V[settingAtoms]==None:
        V[settingAtoms]=True
        break;
  print(S)
  prop = propagateAssignment(S, V, ATOMS)

  return DPHelper(ATOMS, prop, V)

def propagateAssignment(S, V, ATOMS):
  newS = []
  for clauseS in S:
    newC = []
    for literalS in clauseS:
      newC.append(literalS)
    newS.append(newC)

  for littleV in V:
    if V[littleV]==None:
      continue
    if ATOMS[littleV][0] + ATOMS[littleV][1] == 0:
      continue
    removeClause = []
    for clause in newS:
      removeLiteral = []
      for literal in clause:
        if abs(literal)==littleV:
          if V[littleV] == (literal > 0):
            #this will set entire clause to true
            for literals in clause:
              if literals>0:
                ATOMS[littleV][0]-=1
              else:
                ATOMS[littleV][1]-=1

            #remove clause from clauses/ newS
            removeClause.append(clause)
            break
          elif len(clause) == 1:
            #check if only one literal left if so remove from list of clauses
            removeClause.append(clause)
          else:
            #remove literal from list
            removeLiteral.append(clause.index(literal))
            #decrememt atom's count of literals on the atoms
            if literal>0:
              ATOMS[littleV][0]-=1
            else:
              ATOMS[littleV][1]-=1
      for literal in removeLiteral:
        clause.pop(literal)
    for clause in removeClause:
      newS.remove(clause)
    
  return newS
def inputData(iFile):
  oFile = open(iFile,'r')
  lines = oFile.readlines()
  oFile.close()
  fClauses = []
  leftOver = []
  afterZero = False
  for line in lines:
    line = line.replace("\n", "")
    if line[0] in ['0']:
      afterZero = True
    if afterZero:
      leftOver.append(line)
    else:
      fClause = [int(x) for x in line.split()]
      fClauses.append([x for x in fClause])
  fAtoms = {}
  
  for clauseA in fClauses:
    for literal in clauseA:
      key=abs(literal)
      if key not in fAtoms:
        fAtoms[key] = [0, 0]
      
      if literal > 0:
        fAtoms[key][0] +=1

      elif literal < 0:
        fAtoms[key][1] +=1
      
    
  return (fAtoms, fClauses, leftOver)

print("\n")
inputInfo = input('Enter the file name (make sure to add .txt to the end): ')
print("\nGiven Data:\n")
f=open(inputInfo,'r')
print(f.readlines())
f.close()
file2=open("Mooney-Caitlin-A2-Output.txt","w")
print("\nSolved Data:\n")
iAtoms, iClauses, iLeftOver = inputData(inputInfo)
solveData = DP(iAtoms, iClauses)
print("\nSolved:")
for solvingStuff in solveData:
  print(str(solvingStuff)+" "+str(solveData[solvingStuff]))
  file2.write("\n"+str(solvingStuff)+" "+str(solveData[solvingStuff]))
for extraStuff in iLeftOver:
  print(extraStuff)
  file2.write("\n"+extraStuff)

