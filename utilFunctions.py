import random
import pickle
import os


def initNamesList():
    """fonction qui initialise le nom des x joueurs de la partie"""
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
    """fonction qui initialise le cashtab"""
    cashTab ={}
    names = getNameList()
    initialCash = getInitialCash()
    for name in names:
        cashTab[name] = initialCash
    setCashTab(cashTab)

def initMiseTab():
    """fonction qui initialise le cashtab"""
    miseTab ={}
    names = getNameList()
    for name in names:
        miseTab[name] = 0
    setMiseTab(miseTab)


def getNameList():
    """fonction qui recupère la liste des joueurs de la partie"""
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["namesList"])

def getNameListTmp():
    """fonction qui recupère la liste des joueurs encore vivants de la partie"""
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["namesListTmp"])


def getDealer():
    """fonction qui recupère le nom du delaer actuel de la partie"""
    with open('data', 'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    #namesList = data["namesList"]
    #dealerId = data["dealerId"]
    #dealerName = namesList[dealerId]
    dealerName = data['dealerName']
    return(dealerName)

def getPlayerName():
    """fonction qui recupère le nom du joueur"""
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["playerName"])

def getNbPlayers():
    """fonction qui recupère le nombre de joueurs de la partie"""
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["nbPlayers"])

def getInitialCash():
    """fonction qui recupère le montant initial de la cagnotte initiale de chaque joueur"""
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["initialCash"])

def getNbTurns():
    """fonction qui determine le nombre de tours de la partie"""
    with open("data",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data["nbTurns"])

def getCashTab():
    """fonction qui recupere le cashtab actuel de la partie"""
    with open("cashplayers",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data)

def getCashList():
    """fonction qui retourne le cashtab a afficher avec la legende cash"""
    cashTab = getCashTab()
    cashList = []
    for name in cashTab:
        cashList.append(cashTab[name])
    cashList.append("Cash")
    return cashList

def getMiseTab():
    """fonction qui recupere le misetab actuel de la partie"""
    with open("miseplayers",'rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data)

def getMiseList():
    """fonction qui retourne le misetab a afficher avec la legende mise"""
    miseTab = getMiseTab()
    miseList = []
    for name in miseTab:
        miseList.append(miseTab[name])
    miseList.append("Mise")
    return miseList

def setCashTab(cashTab):
    """fonction qui actualise le cashtab"""
    with open('cashplayers','wb') as fichier:
        pickler = pickle.Pickler(fichier)
        pickler.dump(cashTab)

def setMiseTab(miseTab):
    """fonction qui actualise le misetab"""
    with open('miseplayers','wb') as fichier:
        pickler = pickle.Pickler(fichier)
        pickler.dump(miseTab)

def getData():
    """fonction qui recupere le JSON data"""
    with open('data','rb') as fichier:
        unpickler = pickle.Unpickler(fichier)
        data = unpickler.load()
    return(data)

def setData(data):
    """fonction qui actualise le JSON data"""
    with open('data','wb') as fichier:
        pickler = pickle.Pickler(fichier)
        pickler.dump(data)

def biggestInList(list):
    """fonction qui retourne la longueur du plus long mot trouvé dans list"""
    elemMaxLength = 0
    for elem in list:
        if(len(str(elem)) > elemMaxLength):
            elemMaxLength = len(str(elem))
    return(elemMaxLength)

def itemCompletion(item, itemMaxLength):
    """fonction qui complete item par des espaces pour fitter avec itemMaxLength"""
    itemFormated = str(item)
    missingSpaces = itemMaxLength - len(itemFormated)
    for i in range(missingSpaces):
        itemFormated+=" "
    return(itemFormated)

def drawHeaderBorder(headerLength):
    """fonction qui dessine la bordure du header de la partie"""
    headerLine = ""
    for i in range(headerLength):
        headerLine+="#"
    return(headerLine)

def isDealer(name):
    """fonction qui determine si le joueur name est actuelement dealer"""
    dealerName = getDealer()
    if(name == dealerName):
        return("DEALER")
    else:
        return("      ")

def setHeader():
    """fonction qui affiche le header de la partie"""
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
    """fonction qui centre le message au centre du terminal"""
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
    """fonction qui assure que l'utilisateur rentre bien un Int"""
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
