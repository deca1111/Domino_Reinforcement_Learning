import os
import statistics
from collections import deque
from typing import Tuple, List

import torch
import random
import numpy as np
import time
import logging
import pickle

from agent_models.helper import plotMetrics, savePlot
from agent_models.model import Linear_QNet, QTrainer
from dominoObjectOrientedVersion.actionDomino import ActionDomino
from dominoObjectOrientedVersion.dominoGameAI import DominoGameAI
from dominoObjectOrientedVersion.playerdomino import PlayerDomino

MAX_MEMORY = 250_000
BATCH_SIZE = 500
LR = 0.001


class Agent2Player:

    def __init__(self):
        self.game: DominoGameAI = None
        self.nbGame = 0

        self.epsilon = 0.15  # Probabilité de mouvement random
        self.gamma = 0.9  # Discount rate

        self.memory = deque(maxlen=MAX_MEMORY)  # Structure de donnée de typle popLeft()

        self.model = Linear_QNet(60, [256, 512, 256], 56)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def getState(self):
        """
        L'état est un tableau de 60 valeurs
        - 28 valeurs booléennes (ici des entiers 0 ou 1) représentants la main du joueur (présence ou non de chaque pièce)
        - 28 valeurs booléennes (ici des entiers 0 ou 1) représentants le plateau (présence ou non de chaque pièce)
        - 1 entier pour le chiffre à gauche du plateau
        - 1 entier pour le chiffre à droite du plateau
        - 1 entier pour la taille de la pioche
        - 1 entier pour le nombre de pièce dans la main de l'adversaire


        Returns:

        """
        # Initialisation de l'état
        state = [0] * 60

        # AJout de la main du joueur
        for pieceMain in self.game.agentAi.getMainJoueur():
            state[pieceMain.getIndex()] = 1

        # Ajout du plateau
        for piecePlateau in self.game.getPlateau():
            state[28 + piecePlateau.getIndex()] = 1

        state[56] = self.game.plateau[0].getFirstValue()
        state[57] = self.game.plateau[-1].getLastValue()

        # Ajout de la taille de la pioche
        state[58] = len(self.game.getPioche())

        # Ajout de la taille de la main de l'adversaire
        state[59] = self.game.getTailleMainAdverse()[0]

        # return np.array(state, dtype=int)
        return state

    def remember(self, state, action, reward, nextState, done):
        self.memory.append((state, action, reward, nextState, done))

    def trainShortMemory(self, state, action, reward, nextState, done):
        self.trainer.trainStep(state, action, reward, nextState, done)

    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            miniSample = random.sample(self.memory, BATCH_SIZE)
        else:
            miniSample = self.memory

        states, actions, rewards, nextStates, dones = zip(*miniSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)

    def getAction(self, state) -> Tuple[ActionDomino, List[int]]:
        # On veut que epsilon soit de 15% au début et soit réduit à 0% au bout de 1000 manches
        self.epsilon = 0.15 * ((5000 - self.nbGame) / 5000)

        # Une action donnée par le modèle est une liste de 56 valeurs
        actionList = [0] * 56
        actionObject = None

        # On choisit une action aléatoire avec une probabilité epsilon
        if random.random() <= self.epsilon:
            actionObject = random.choice(self.game.getPossibleAction())
            actionList[actionObject.getIndexValue()] = 1
        # Sinon on prend l'action choisie par le modèle
        else:
            # Conversion de l'état en tensor
            stateTensor = torch.tensor(state, dtype=torch.float)
            # Prédiction du modèle
            prediction = self.model(stateTensor)
            prediction = prediction.tolist()

            # Nettoyage des action illégales
            indexActionPossible = [action.getIndexValue() for action in self.game.getPossibleAction()]
            for indexPred in range(len(prediction)):
                if indexPred not in indexActionPossible:
                    prediction[indexPred] = np.nan

            # Récupération de l'index de l'action choisie
            actionIndex = np.nanargmax(prediction)
            # Création de l'action
            actionList[actionIndex] = 1
            for action in self.game.getPossibleAction():
                if actionIndex == action.getIndexValue():
                    actionObject = action
                    break

        return actionObject, actionList

    def saveMemory(self, fileName):
        with open(fileName, 'wb') as handle:
            pickle.dump(self.memory, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def startTraining(self, maxNbGame: int, nomModelToSave: str):
        self.nbGame = 0

        racineSave = "./agent_models/savedModel/"
        racineSave = os.path.join(racineSave, nomModelToSave)

        # Si le dossier de sauvegarde n'existe pas, on le crée
        if not os.path.exists(racineSave):
            os.makedirs(racineSave)

        logFileName = "agent_models/logs/logs_training_2players.log"
        logging.basicConfig(filename=logFileName, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

        logging.warning(f"Start training : {maxNbGame} games")

        last100Games = []
        plotMeanProportionVictoire = []
        plotXMeanProportionVictoire = []
        plotProportionVictoire = []
        plotXProportionVictoire = []
        totalClassement = 0
        totalVictoire = 0

        # Initialisation de la partie
        opponentRandom = PlayerDomino("PlayerRandom1")
        self.game = DominoGameAI([opponentRandom], display=False)
        self.game.resetTraining()

        startTime = time.time()
        start100Game = time.time()
        duree100games = []

        while self.nbGame < maxNbGame:
            # Récupération de l'état actuel
            currentState = self.getState()

            # Choix de l'action à jouer
            actionObject, actionList = self.getAction(currentState)

            # On joue l'action
            reward, gameOver, classement = self.game.playStep(actionObject)

            # On récupère le nouvel état
            newState = self.getState()

            # Entrainement de la mémoire court terme
            self.trainShortMemory(currentState, actionList, reward, newState, gameOver)

            # Mémorisation
            self.remember(currentState, actionList, reward, newState, gameOver)

            if gameOver:
                # Reset de la manche
                self.game.resetTraining()
                self.nbGame += 1

                # Entrainement de la mémoire long terme (experience replay)
                self.trainLongMemory()

                totalVictoire += 1 if classement == 1 else 0
                last100Games.append(1 if classement == 1 else 0)
                # plotClassement.append(classement)
                # totalClassement += classement
                # plotMeanClassement.append(totalClassement / self.nbGame)

                if self.nbGame % 10 == 0:
                    plotProportionVictoire.append(totalVictoire / self.nbGame)
                    plotXProportionVictoire.append(self.nbGame)

                if self.nbGame % 100 == 0:
                    plotMeanProportionVictoire.append(statistics.mean(last100Games))
                    plotXMeanProportionVictoire.append(self.nbGame)
                    last100Games = []

                    now = time.time()
                    duree100games.append(now - start100Game)
                    secondes100gamesMean = int(statistics.mean(duree100games))
                    minutes100gamesMean = int(secondes100gamesMean // 60)
                    secondes = int(now - startTime)
                    heures = int(secondes // 3600)
                    minutes = int((secondes // 60) % 60)
                    message = (f"[Game {self.nbGame}] - Temps total écoulé: {heures}:{minutes}:{secondes % 60} "
                               f"- Temps moyen 100 games: {minutes100gamesMean}:{secondes100gamesMean % 60} "
                               f"- % victoire _Global_ {round(plotProportionVictoire[-1], 5)}% "
                               f"_100 last_ {round(plotMeanProportionVictoire[-1], 5)}% "
                               f"- Remplissage mémoire {round(len(self.memory) / MAX_MEMORY * 100, 2)}%")
                    print(message)
                    logging.info(message)

                    plotMetrics(plotXProportionVictoire, plotProportionVictoire,
                                plotXMeanProportionVictoire, plotMeanProportionVictoire)

                    start100Game = time.time()

                    if len(self.memory) > MAX_MEMORY:
                        break

                if self.nbGame % 1000 == 0 and self.nbGame != 0:
                    self.model.save(os.path.join(racineSave, f"{nomModelToSave}_model.pth"))

        # Sauvegarde finale
        savePlot(plotXProportionVictoire, plotProportionVictoire,
                 plotXMeanProportionVictoire, plotMeanProportionVictoire,
                 os.path.join(racineSave, "plotMetrics.png"))
        self.saveMemory(os.path.join(racineSave, f"savedMemory_{len(self.memory)}_{MAX_MEMORY}.pickle"))
        self.model.save(os.path.join(racineSave, f"{nomModelToSave}_model.pth"))
