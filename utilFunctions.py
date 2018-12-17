import random
import pickle
import os


def initNamesList():
    with open("dicoNames.txt",'r') as fichier:
        contenu = fichier.readlines()
    nameList = []
    dicoNames =[]
    nameList.append(getPlayerName())
    for name in contenu:
        dicoNames.append(name)
    nbPlayers = getNbPlayers()-1
    for i in range(nbPlayers):
        r =random.randint(0,len(dicoNames)-1)
        print(dicoNames[r])
        print(len(dicoNames[r])-1)
        nameList.append(dicoNames[r][0:len(dicoNames[r])-1])
        dicoNames.remove(dicoNames[r])
    data = getData()
    data["namesList"] =nameList
    setData(data)

def initCashTab():
    cashTab ={}
    names = getNameList()
    initialCash = getInitialCash()
    for name in names:
        cashTab[name] = initialCash
    setCashTab(cashTab)

def initMiseTab():
    miseTab ={}
    names = getNameList()
    for name in names:
        miseTab[name] = 0
    setMiseTab(miseTab)


def getNameList():
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["namesList"])

def getNameListTmp():
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["namesListTmp"])


def getDealer():
    with open('data', 'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    #namesList = data["namesList"]
    #dealerId = data["dealerId"]
    #dealerName = namesList[dealerId]
    dealerName = data['dealerName']
    return(dealerName)

def getPlayerName():
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["playerName"])

def getNbPlayers():
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["nbPlayers"])

def getInitialCash():
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["initialCash"])

def getNbTurns():
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["nbTurns"])

def getCashTab():
    with open("cashplayers",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data)

def getCashList():
    cashTab = getCashTab()
    cashList = []
    for name in cashTab:
        cashList.append(cashTab[name])
    cashList.append("Cash")
    return cashList

def getMiseTab():
    with open("miseplayers",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data)

def getMiseList():
    miseTab = getMiseTab()
    miseList = []
    for name in miseTab:
        miseList.append(miseTab[name])
    miseList.append("Mise")
    return miseList

def setCashTab(cashTab):
    with open('cashplayers','wb') as fichier:
        pickler = pickle.Pickler(fichier)
        pickler.dump(cashTab)

def setMiseTab(miseTab):
    with open('miseplayers','wb') as fichier:
        pickler = pickle.Pickler(fichier)
        pickler.dump(miseTab)

def getData():
    with open('data','rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data)

def setData(data):
    with open('data','wb') as fichier:
        pickler = pickle.Pickler(fichier)
        pickler.dump(data)

def biggestInList(list):
    elemMaxLength = 0
    for elem in list:
        if(len(str(elem)) > elemMaxLength):
            elemMaxLength = len(str(elem))
    return(elemMaxLength)

def itemCompletion(item, itemMaxLength):
    itemFormated = str(item)
    missingSpaces = itemMaxLength - len(itemFormated)
    for i in range(missingSpaces):
        itemFormated+=" "
    return(itemFormated)

def drawHeaderBorder(headerLength):
    headerLine = ""
    for i in range(headerLength):
        headerLine+="#"
    return(headerLine)

def isDealer(name):
    dealerName = getDealer()
    if(name == dealerName):
        return("DEALER")
    else:
        return("      ")

def setHeader():
    os.system("clear")
    nameList = getNameListTmp()
    nameList.append("Names")
    cashList = getCashList()
    miseList = getMiseList()
    cashTab = getCashTab()
    miseTab = getMiseTab()
    nameMaxLength = biggestInList(nameList)
    nameList.remove("Names")
    cashMaxLength = biggestInList(cashList)
    miseMaxLength = biggestInList(miseList)
    headerLegend = "#              {}    {}    {}    #".format(itemCompletion("Names",nameMaxLength),itemCompletion("Cash",cashMaxLength), itemCompletion("Mise", miseMaxLength) )
    headerLength = len(headerLegend)
    print(centerText(drawHeaderBorder(headerLength)))
    print(centerText(headerLegend))
    for name in nameList:
        nameFormated = itemCompletion(name, nameMaxLength)
        cashFormated = itemCompletion(cashTab[name], cashMaxLength)
        miseFormated = itemCompletion(miseTab[name], miseMaxLength)
        print(centerText("#    {}    {}    {}    {}    #".format(isDealer(name),nameFormated,cashFormated, miseFormated)))
    print(centerText(drawHeaderBorder(headerLength)))

def centerText(message):
    rows,columns = os.popen("stty size",'r').read().split()
    textWidth = len(message)
    textCenter = ""
    numberSpaces = (int(columns) - textWidth) // 2
    for i in range(numberSpaces):
        textCenter += " "
    textCenter += message
    #for i in range(numberSpaces):
    #    textCenter += " "
    return(textCenter)

def secureInputInt(message):
    result = 0
    resultOk = False
    while(not(resultOk)) :
        result = input(message)
        try:
            result = int(result)
            resultOk = True;
            break
        except ValueError:
            pass
    return (result)
