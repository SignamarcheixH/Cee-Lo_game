import gameFunctions
import utilFunctions
import pickle
import os


data = { "playerName" : "VOUS",
              "nbPlayers" : 5,
              "initialCash" : 2000,
              "namesList" :  ["VOUS","NORD","SUD","EST","OUEST"],
              "namesListTmp" : [],
              "nbPlayersTmp" : [],
              "dealerId" : 2,
              "dealerName" : "",
              "nbTurns" : 3,}


def optionMenu():
    stay = True
    while(stay):
        os.system("clear")
        data = utilFunctions.getData()
        print(utilFunctions.centerText("OPTIONS"))
        print("")
        print(utilFunctions.centerText("(1) Nom du Joueur : {}".format(utilFunctions.getPlayerName())))
        print(utilFunctions.centerText("(2) Nombre de joueurs : {}".format(utilFunctions.getNbPlayers())))
        print(utilFunctions.centerText("(3) Cash en début de partie : {}".format(utilFunctions.getInitialCash())))
        print(utilFunctions.centerText("(4) Nombre de tours de jeu  : {}".format(utilFunctions.getNbTurns())))
        print(utilFunctions.centerText("(5) Quitter"))
        print("")
        response = utilFunctions.secureInputInt(utilFunctions.centerText("Que voulez-vous faire ? "))
        if(response == 1):
            newName = str(input(utilFunctions.centerText("Quel est votre nouveau nom de joueur ? ")))
            data["playerName"] = newName.upper()
        if(response == 2):
            newNbPlayers = utilFunctions.secureInputInt(utilFunctions.centerText("Combien de joueurs voulez-vous ? "))
            data["nbPlayers"] = newNbPlayers
        if(response == 3):
            newInitialCash = utilFunctions.secureInputInt(utilFunctions.centerText("Avec combien d'€ voulez-vous commencer ? "))
            data['initialCash'] = newInitialCash
        if(response == 4):
            newNbTurns = utilFunctions.secureInputInt(utilFunctions.centerText("En combien de tours se déroulera la partie ? "))
            data['nbTurns'] = newNbTurns
        if(response == 5):
            stay = False
        utilFunctions.setData(data)


def mainMenu():
    play = True
    while(play):
        os.system("clear")
        print(utilFunctions.centerText("Welcome to the Cee-Lo downtown !"))
        print(utilFunctions.centerText("Que souhaitez-vous faire ?"))
        print(utilFunctions.centerText("(1) : Match à mort"))
        print(utilFunctions.centerText("(2) : Partie en {} tours".format(utilFunctions.getNbTurns())))
        print(utilFunctions.centerText("(3) : Options"))
        print(utilFunctions.centerText("(4) : Règles du Cee-Lo"))
        print(utilFunctions.centerText("(5) : Quitter"))
        print("")
        response = utilFunctions.secureInputInt(utilFunctions.centerText("Que choisissez-vous ? "))
        if (response == 1):
            utilFunctions.initNamesList()
            gameFunctions.runDeathGame()
        if (response == 2):
            utilFunctions.initNamesList()
            gameFunctions.runNbTurnsGame()
        if (response == 3):
            optionMenu()
        if (response == 4):
            print(1)
        if (response == 5):
            play = False

utilFunctions.setData(data)
mainMenu()
