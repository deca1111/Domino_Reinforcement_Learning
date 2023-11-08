import random
from typing import List, Tuple
import builtins

from actionDomino import ActionDomino
from pieceDomino import PieceDomino


class PlayerDomino:
    """
    Represents a player in a domino game.

    Args:
        nom: The name of the player (default: "Bob").
        mainJoueur: The player's hand (default: an empty list).

    Methods:
        computeAction: Computes the player's action given the current game state.
        getMainJoueur: Returns the player's hand.

    Returns:
        int: The index of the chosen action.

    """

    def __init__(self, nom: str = "Bob", idJoueur: int = None, mainJoueur=None):
        self.nom = nom
        if mainJoueur is None:
            mainJoueur = []
        self.mainJoueur = mainJoueur
        self.id = builtins.id(self) if idJoueur is None else idJoueur
        self.score = 0

    def chooseAction(
            self, plateau: List[PieceDomino], taillePioche: int,
            tailleMainAdverse: List[int], possibleAction: List[ActionDomino]
            ) -> ActionDomino:
        return random.choice(possibleAction)

    def getMainJoueur(self) -> List[PieceDomino]:
        return self.mainJoueur

    def setMainJoueur(self, mainJoueur: List[PieceDomino]):
        self.mainJoueur = mainJoueur

    def emptyMainJoueur(self):
        self.mainJoueur = []

    def appendMainJoueur(self, piece: PieceDomino):
        self.mainJoueur.append(piece)

    def removePieceFromHand(self, piece: PieceDomino):
        self.mainJoueur.remove(piece)

    def getName(self):
        return self.nom

    def setScore(self, score: int):
        self.score = score

    def addScore(self, score: int):
        self.score += score

    def getScore(self) -> int:
        return self.score
