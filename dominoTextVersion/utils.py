import random
from itertools import combinations_with_replacement
from typing import List, Tuple, Dict

# Création de la liste de toutes les pièces
listPiece = list(combinations_with_replacement(range(7), 2))


class ActionNotValidError(Exception):
    """
    Exception raised when an invalid action is encountered.

    Args:
        action: The invalid action that caused the exception.
        message: Optional. A custom error message.

    Attributes:
        action: The invalid action that caused the exception.
        message: The error message associated with the exception.
    """

    def __init__(self, action, message="Impossible action"):
        self.action = action
        self.message = message
        super().__init__(self.message)


def initCorrespondance() -> Tuple[Dict, Dict]:
    """
    Initializes the correspondence dictionaries for piece sides and their corresponding actions.

    Returns:
        A tuple containing two dictionaries:
        - pieceSideToIndexAction: A dictionary mapping piece sides (represented by a tuple of piece and side) to their corresponding action indices.
        - indexActionToPieceSide: A dictionary mapping action indices to their corresponding piece sides (represented by a tuple of piece and side).

    """
    pieceSideToIndexAction = {}
    indexActionToPieceSide = {}
    for index in range(len(listPiece) * 2):
        side = 'G' if index % 2 == 0 else 'D'
        pieceSide = (listPiece[index // 2], side)
        indexActionToPieceSide[index] = pieceSide
        pieceSideToIndexAction[pieceSide] = index

    return pieceSideToIndexAction, indexActionToPieceSide


pieceSideToIndexAction, indexActionToPieceSide = initCorrespondance()


def generatePossibleAction(plateau: List[Tuple], main: List[Tuple]) -> List[int]:
    """
    Génère une liste d'indices d'actions possibles en fonction du plateau et des pièces principales donnés.

    Args:
        plateau: Une liste de tuples représentant l'état actuel du plateau.
        main: Une liste de tuples représentant les pièces principales du joueur.

    Returns:
        Une liste d'entiers représentant les indices d'actions possibles.

    """
    possibleAction = []
    for piece in main:
        # Si la pièce peut être posée à gauche on ajoute l'action
        if plateau[0][0] in piece:
            possibleAction.append(getIndexActionFromPiece(piece, 'G'))

        # Si la pièce peut être posée à droite on ajoute l'action
        if plateau[-1][1] in piece:
            possibleAction.append(getIndexActionFromPiece(piece, 'D'))

    return possibleAction


def getIndexActionFromPiece(piece: Tuple, side: chr) -> int:
    """
    Returns the action index corresponding to the given piece and side.

    Args:
        piece: A tuple representing the piece.
        side: A character representing the side of the piece.

    Returns:
        An integer representing the action index.

    Raises:
        KeyError: If the given piece and side combination is not found in the correspondence dictionary.
    """

    return pieceSideToIndexAction[(piece, side)]


def getPieceFromIndexAction(indexAction: int) -> Tuple[Tuple, bool]:
    """
    Returns the piece and side corresponding to the given action index.

    Args:
        indexAction: An integer representing the action index.

    Returns:
        A tuple containing the piece and side as follows:
        - piece: A tuple representing the piece.
        - side: A boolean indicating the side of the piece (True for right, False for left).

    Raises:
        KeyError: If the given action index is not found in the correspondence dictionary.
    """

    return indexActionToPieceSide[indexAction]


def pickRandomAction(actionPossible: List[int]) -> int:
    """
    Picks a random action from the list of possible actions.

    Args:
        actionPossible: A list of integers representing the possible actions.

    Returns:
        An integer representing the randomly chosen action.
    """

    return random.choice(actionPossible)


def computeAction(plateau: List[Tuple], mainJoueur: List[Tuple], action: int) -> Tuple[List[Tuple], List[Tuple]]:
    """
    Computes the updated plateau and player's hand after performing the given action.

    Args:
        plateau: A list of tuples representing the current state of the plateau.
        mainJoueur: A list of tuples representing the player's hand.
        action: An integer representing the action to be performed.

    Returns:
        A tuple containing the updated plateau and the updated player's hand as lists of tuples.

    Raises:
        ActionNotValidError: If the given action is not valid for the current state of the plateau.
    """

    # On essaye de convertir l'index d'action en piece et side correspondant, si c'est impossible on raise un erreur
    try:
        piece, side = getPieceFromIndexAction(action)
    except Exception as e:
        raise ActionNotValidError(action) from e

    # Calcul du plateau mis à jour
    # Si on veut jouer à gauche
    if side == 'G':
        if piece[1] == plateau[0][0]:
            plateau.insert(0, piece)
        elif piece[0] == plateau[0][0]:
            plateau.insert(0, piece[::-1])
        else:
            raise ActionNotValidError(action)
    # Sinon, si on veut jouer à droite
    elif piece[0] == plateau[-1][1]:
        plateau.append(piece)
    elif piece[1] == plateau[-1][1]:
        plateau.append(piece[::-1])
    else:
        raise ActionNotValidError(action)

    # On enleve la pièce de la main du joueur
    mainJoueur.remove(piece)

    return plateau, mainJoueur


def computeScores(mainsJoueurs: List[List[Tuple]], scoresJoueurs: List[float]) -> List[float]:
    """
    Computes the updated scores for each player based on their hands.

    Args:
        mainsJoueurs: A list of lists, where each inner list represents the hand of a player.
        scoresJoueurs: A list of floats representing the current scores of each player.

    Returns:
        A list of floats representing the updated scores for each player.
    """

    # Pour chaque joueur, on additionne
    for joueur, main in enumerate(mainsJoueurs):
        scoresJoueurs[joueur] += sum(x + y for x, y in main)

    return scoresJoueurs
