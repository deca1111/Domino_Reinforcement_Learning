import copy
import random
from itertools import combinations_with_replacement, product
from typing import List

from dominoGame import PlayersListError, DominoGame
from pieceDomino import PieceDomino
from playerdomino import PlayerDomino


class DominoGameAI(DominoGame):
    def __init__(self, listOpponent: List[PlayerDomino], display=False, seed: int = None):

        self.nbPlayer = len(listOpponent)+1
        if self.nbPlayer not in {2, 3, 4}:
            raise PlayersListError("Number of player opponent must be 1,2 or 3")

        self.listOpponent = listOpponent

        self.agentAi = PlayerDomino("AI-TrainingAgent")

        # L'agent est le dernier de la liste de joueurs
        listPlayer = listOpponent + [self.agentAi]

        super().__init__(listPlayer=listPlayer, seed=seed, display=display)

        self.resetTraining()

    def resetTraining(self):
        self.resetGame()

        self.isTrainingGameOver = False

        if self.display:
            print(f"\n===== Début d'une manche d'entrainement =====")
            print(f"Le joueur {self.listPlayer[self.indexPremierJoueur].getName()} a la plus grande "
                  f"pièce : {self.plateau[0].toString()}")

        # On avance dans la partie jusqu'à ce que ça soit à l'agent de jouer:
        joueurActuel = self.listPlayer[(self.indexPremierJoueur + self.indexJoueurTour) % self.nbPlayer]

        while joueurActuel != self.agentAi:
            self.playTurnJoueur(joueurActuel)

            joueurActuel = self.listPlayer[(self.indexPremierJoueur + self.indexJoueurTour) % self.nbPlayer]
