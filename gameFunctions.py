import random
#import main
import utilFunctions

#############################################################################
#################### GAME FUNCTIONS ############################################
#############################################################################


def tirage_des():
    """Fonction qui simule un lancer de trois dés"""
    L=[]
    for i in range(3):
        L.append(random.randint(1,6))
    return(L)



def rec_main(tirage):
    """fonction qui donne le score de la main actuelle, suivant le modèle suivant
        Type de main |  Score
                111 -> 13
                666 -> 12
                555 -> 11
                444 -> 10
                333 ->  9
                222 ->  8
                {456} ->  7
                {bAb} ->  A  (de 6 a 1)
                {123}  ->  0
                {ABC} -> -404
    """
    nbDesIdentiques=0
    for i in range(1,7):
        if(tirage.count(i)>nbDesIdentiques):
            nbDesIdentiques=tirage.count(i)
            valeurDe=i

    if(nbDesIdentiques==3)&(valeurDe==1):
        return(13)

    elif (nbDesIdentiques==3):
        return(6+valeurDe)

    elif (nbDesIdentiques ==2):
        for elem in tirage:
            if(elem != valeurDe):
                return(elem)

    elif (4 in tirage) & (5 in tirage) & (6 in tirage):
        return(7)

    elif (1 in tirage) & (2 in tirage) & (3 in tirage):
        return(0)
    else:
        return(-404)




def rec_jeu():
    """fonction qui réalise les trois lancers autorisés, et qui renvoie le premier score obtenu"""
    for i in range(2): #on ne realise que deux lancers d'abord, car on renverra forcement le score du troisième
        main=tirage_des()
        input(utilFunctions.centerText("Lancer {} : {}".format(i+1,main)))
        if (rec_main(main)!=-404): #si on a rien obtenu, on est autorisé a relancer, mais si on a ne serait-ce que 0 points, on doit le garder
            print(utilFunctions.centerText("{} donne un score de {} au Cee-Lo !".format(main,rec_main(main))))
            return(rec_main(main))

    main=tirage_des()
    input(utilFunctions.centerText("Lancer 3 : {}".format(main)))
    print(utilFunctions.centerText("{} donne un score de {} au Cee-Lo !".format(main,rec_main(main))))
    return(rec_main(main))




def scoretocoeff(score):
    """fonction qui determine le coefficient multiplicateur de la mise en fonction du score"""
    if score ==13:		#cas Snake Eyes {111}
        return(5)
    elif (score == 12) | (score == 11) | (score == 10) | (score == 9) | (score == 8):  #Cas {aaa} sauf a=1
        return(4)
    elif score == 7: #Cas {456}
        return(3)
    elif (score == 6) | (score == 5) | (score == 4) | (score == 3) | (score == 2) | (score == 1):  #Cas {AAB}
        return(2)
    else:				#englobe les cas ou score = 0 {123} (car c'est lors du tirage de cette combinaison sur l'on double la mise)
        return(1)		# et score =-404  (car alors on a juste perdu sa mise, donc *1)





def dealer_turn():
    """fonction qui gère le tour du DEALER"""
    dealerName = utilFunctions.getDealer()
    cashTab = utilFunctions.getCashTab()
    miseTab = utilFunctions.getMiseTab()
    namesList = utilFunctions.getNameListTmp()
    print(utilFunctions.centerText("Le dealer : {} joue".format(dealerName)))
    score_dealer=rec_jeu()
    if score_dealer == 0:				#Si le dealer tire {123}, il doit doubler la mise de tout les joueurs
        print(utilFunctions.centerText("Le dealer {} obtient 1,2,3 ! Il double la mise de tout le monde ! ".format(dealerName)))
        for name in namesList:
            if name == dealerName:			#il ne fait rien sur sa mise ( qui est de 0.0 forcement)
                pass
            else:					#et double celle des autres, quitte a passer en négatif
                cashTab[dealerName]-=miseTab[name]
                miseTab[name]*=2
                utilFunctions.setCashTab(cashTab)
                utilFunctions.setMiseTab(miseTab)
    return(score_dealer)





def allTurns(dealerScore):
    nameList = utilFunctions.getNameListTmp()
    dealerName = utilFunctions.getDealer()
    for name in nameList:
        if name == dealerName:
            pass
        else:
            print(utilFunctions.centerText("Tour de {}".format(name)))
            joueurVsDealer(name,dealerScore)
            input()
        utilFunctions.setHeader()





def joueurVsDealer(name,dealerScore):
    """fonction qui gère un affrontement entre un joueur et le dealer, prend en argument le numero du joueur actuel et le score du dealer actuel"""
    cashTab = utilFunctions.getCashTab()
    miseTab = utilFunctions.getMiseTab()
    dealerName = utilFunctions.getDealer()
    joueurScore=rec_jeu()      #On tire la main du joueur et on en déduit son score
    print(utilFunctions.centerText("{} a obtenu {} !".format(name,joueurScore)))

    if joueurScore==0:					#Si le joueur a tiré {123}, il se voit obligé de doubler sa mise
        print(utilFunctions.centerText("Double la mise !"))
        if (cashTab[name] < miseTab[name]):      #Cas ou le joueur ne peut pas doubler sa mise
            miseTab[name]+=cashTab[name]
            cashTab[name] = 0
        else:							 #Cas ou il a assez d'argent pour doubler
            cashTab[name]-=miseTab[name]
            miseTab[name]*=2

    if joueurScore < dealerScore:			#Cas ou le dealer gagne

        print(utilFunctions.centerText("{} perd face au dealer, il perd {}*{}, soit {}€ !".format(name,miseTab[name],scoretocoeff(dealerScore),miseTab[name]*scoretocoeff(dealerScore))))
        dette=miseTab[name]*scoretocoeff(dealerScore)   #La dette est la somme que doit payer le joueur au dealer
        if dette > (cashTab[name]+miseTab[name]):					#Si elle est superieure au total (cashtab+mise) du joueur
            cashTab[dealerName]=cashTab[dealerName]+cashTab[dealerName]+miseTab[name]   #Le dealer empoche la totalité de l'argent du joueur (cashtab+mise)
            cashTab[name]=0											#et le joueur est a 0 (il ne peut pas être en négatif)
        else:												#sinon
            cashTab[name]=(cashTab[name]-dette)+ miseTab[name]				#le joueur voit son solde déduit de la dette mais récupère sa mise
            cashTab[dealerName]+=dette									#le dealer empoche la dette


    elif joueurScore >dealerScore:		#Cas ou le dealer perd

        print(utilFunctions.centerText("Le dealer s'écroule face a {}, il perd {}*{}, soit {}€ !".format(name,miseTab[name],scoretocoeff(joueurScore),miseTab[name]*scoretocoeff(joueurScore))))
        dette=miseTab[name]*scoretocoeff(joueurScore) 	#la dette est la somme que doit le dealer au joueur pour ce tour
        if dette > cashTab[dealerName]:			#Cas ou le dealer ne peut rembourser la dette en entier
            if cashTab[dealerName] < 0:				#Si le dealer est deja endeté
                cashTab[name]+=miseTab[name]				#le joueur reprend simplement sa mise
            else:								#sinon
                cashTab[name]=cashTab[name]+cashTab[dealerName]+miseTab[name]   #Le joueur prend l'integralité du cashtab du dealer et reprend sa mise
        else:								#Cas ou le dealer a suffisamment d'argent pour payer
            cashTab[name]=cashTab[name]+dette+miseTab[name]					#le joueur empoche la dette et reprend sa mise
        cashTab[dealerName]-=dette				#Dans tous les cas, le dealer s'alourdit de la dette (il peut être en négatif pendant son tour, lui)


    else:									#Cas d'égalité entre le joueur et le dealer
        print(utilFunctions.centerText("Egalité, {} reprend sa mise".format(name)))
        cashTab[name]+=miseTab[name]				#le joueur reprend sa mise

    utilFunctions.setCashTab(cashTab)
    utilFunctions.setMiseTab(miseTab)



def fullTurn():
    utilFunctions.setHeader()
    utilFunctions.initMiseTab()
    miseAll()
    dealerScore = dealer_turn()
    allTurns(dealerScore)
    losersElim()
    input()


def losersElim():
    cashTab = utilFunctions.getCashTab()
    miseTab = utilFunctions.getMiseTab()
    listeLosers = []
    for name in cashTab:
        if(cashTab[name] <= 0):
            print(utilFunctions.centerText("{} n'a plus d'argent, il est eliminé".format(name)))
            listeLosers.append(name)
    data = utilFunctions.getData()
    dealerId = data["dealerId"]
    nameList =data["namesListTmp"]
    dealerId = (dealerId+1)%(len(nameList))
    while(nameList[dealerId] in listeLosers):
        dealerId = (dealerId+1)%(len(nameList))
    data['dealerId'] = dealerId
    dealerName = nameList[dealerId]
    data['dealerName'] = dealerName
    for loser in listeLosers:
        nameList.remove(loser)
        data['namesListTmp'] = nameList
        for i in range (len(nameList)):
            if(nameList[i] == dealerName):
                data["dealerId"] = i
        data['nbPlayersTmp']-=1
        cashTab.pop(loser)
        miseTab.pop(loser)
    utilFunctions.setData(data)
    utilFunctions.setCashTab(cashTab)
    utilFunctions.setMiseTab(miseTab)



def runNbTurnsGame():
    utilFunctions.initCashTab()
    utilFunctions.initMiseTab()
    nbTurns =utilFunctions.getNbTurns()
    data = utilFunctions.getData()
    data['namesListTmp'] = list(data['namesList'])
    data['nbPlayersTmp'] = data['nbPlayers']
    data['dealerId'] = random.randint(0,data['nbPlayers']-1)
    data['dealerName'] = data['namesList'][data['dealerId']]
    utilFunctions.setData(data)
    for i in range(nbTurns):
        fullTurn()
    cashTab = utilFunctions.getCashTab()
    nameWinner = ""
    cashWinner = 0
    for name in cashTab:
            if(cashTab[name] > cashWinner):
                cashWinner = cashTab[name]
                nameWinner = name
    print(utilFunctions.centerText("Le gagnant est {}, il a remporté {}€ !".format(nameWinner,cashWinner)))
    input()

def runDeathGame():
    utilFunctions.initCashTab()
    utilFunctions.initMiseTab()
    cashTab = utilFunctions.getCashTab()
    data = utilFunctions.getData()
    data['namesListTmp'] = list(data['namesList'])
    data['nbPlayersTmp'] = data['nbPlayers']
    data['dealerId'] = random.randint(0,data['nbPlayers']-1)
    data['dealerName'] = data['namesList'][data['dealerId']]
    utilFunctions.setData(data)
    while(len(cashTab) != 1):
        fullTurn()
        cashTab =utilFunctions.getCashTab()
    for winner in cashTab:
        nameWinner = winner
        cashWinner = cashTab[winner]
    print(utilFunctions.centerText("{} est le seul survivant de Cee-Lo, il a gagné {}€".format(nameWinner,cashWinner)))
    input()


#############################################################################
################  ADVERSARY FUNCTIONS ############################################
#############################################################################

def miseAdversary(name):
    """fonction qui simule la mise d'un adversaire"""
    cashTab = utilFunctions.getCashTab()
    miseTab = utilFunctions.getMiseTab()
    sup = cashTab[name]
    mise=random.randint(1,sup)
    cashTab[name] = cashTab[name] - mise
    miseTab[name] = mise
    utilFunctions.setCashTab(cashTab)
    utilFunctions.setMiseTab(miseTab)
    print(utilFunctions.centerText("{} mise {}€ !".format(name, mise)))


def miseAll():
    cashTab = utilFunctions.getCashTab()
    playerName = utilFunctions.getPlayerName()
    dealerName = utilFunctions.getDealer()

    for name in cashTab:
        if(name == dealerName):
            pass
        else:
            print(utilFunctions.centerText("{} est en train de miser".format(name)))
            if(name == playerName):
                misePlayer()
            else:
                miseAdversary(name)
            input()
        utilFunctions.setHeader()





#############################################################################
##################  PLAYER FUNCTIONS  ############################################
#############################################################################

def misePlayer():
    """fonction qui gère la mise du joueur"""

    playerName = utilFunctions.getPlayerName()
    cashTab = utilFunctions.getCashTab()
    miseTab = utilFunctions.getMiseTab()
    cashMax = cashTab[playerName]
    MISEFLAG = False

    while MISEFLAG != True:
        print(utilFunctions.centerText("Vous avez {} €\n".format(cashMax)))
        mise = utilFunctions.secureInputInt(utilFunctions.centerText("Combien souhaitez-vous miser ce tour-ci ?\n"))
        if (mise >= 1) & (mise <= cashMax):
            cashTab[playerName] = cashTab[playerName] - mise
            miseTab[playerName] = mise
            utilFunctions.setCashTab(cashTab)
            utilFunctions.setMiseTab(miseTab)
            MISEFLAG=True
            print(utilFunctions.centerText("Vous misez {} €".format(mise)))
        else:
            print(utilFunctions.centerText("Vous n'avez pas cette somme"))
