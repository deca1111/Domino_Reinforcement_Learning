import copy
import random
from itertools import combinations_with_replacement, product
from typing import List

from actionDomino import ActionDomino
from pieceDomino import PieceDomino
from playerdomino import PlayerDomino


class DominoGame:
    """
    Represents a game of dominoes.

    Args:
        listPlayer: A list of PlayerDomino objects representing the players in the game.
        scoreMax: An integer representing the maximum score to reach in the game (default: 150).
        display: A boolean indicating whether to display game information during gameplay (default: True).
        seed: An integer used to seed the random number generator for shuffling the domino pieces (default: None).

    Raises:
        PlayersListError: If the number of players is not 2, 3, or 4.

    Attributes:
        nbPlayer: An integer representing the number of players in the game.
        listPlayer: A list of PlayerDomino objects representing the players in the game.
        scoreMax: An integer representing the maximum score to reach in the game.
        display: A boolean indicating whether to display game information during gameplay.
        listPiece: A list of PieceDomino objects representing the domino pieces in the game.
        nbPiecesDistrib: An integer representing the number of pieces to distribute to each player.
        indexManche: An integer representing the current round index.
        isGameOver: A boolean indicating whether the game is over.
        indexPremierJoueur: An integer representing the index of the player with the highest scoring piece.
        plateau: A list of PieceDomino objects representing the game board.
        indexTour: An integer representing the current turn index.
        isMancheOver: A boolean indicating whether the round is over.
        indexJoueurTour: An integer representing the index of the player whose turn it is.
        isTourOver: A boolean indicating whether the turn is over.
        nbPass: An integer representing the number of players who have passed their turn.
        pioche: A list of PieceDomino objects representing the remaining domino pieces in the game.

    Methods:
        resetGame: Resets the game by resetting the scores and the round index, and calls resetManche().
        resetManche: Resets the round by distributing the dominoes, finding the first piece, and initializing the game board.
        resetTurn: Resets the turn by resetting the current player index and the turn status.
        distribDominoes: Distributes the domino pieces to each player.
        verifSeries: Checks if there is a series of domino pieces in the players' hands.
        playGame: Plays the game until it is over.
        playManche: Plays a round of the game.
        playTurn: Plays a turn of the game.
        playTurnJoueur: Plays a turn for a specific player.
        generatePossibleAction: Generates a list of possible actions for the current player.
        computeAction: Computes the action chosen by the player.
        updateScores: Updates the scores of the players.
        printPlateau: Prints the current game board.
    """

    def __init__(self, listPlayer: List[PlayerDomino], scoreMax=150, display=True, seed: int = None):

        self.nbPlayer = len(listPlayer)
        if self.nbPlayer not in {2, 3, 4}:
            raise PlayersListError("Number of player must be 2,3 or 4")

        self.listPlayer = listPlayer

        self.scoreMax = scoreMax

        self.display = display

        if seed is not None:
            random.seed(seed)

        # Création de la liste des pièces
        self.listPiece = []
        self.listPiece.extend(
            PieceDomino(values=listValues, index=index)
            for index, listValues in enumerate(list(combinations_with_replacement(range(7), 2)))
            )

        # Nombre de pièces à distribuer
        self.nbPiecesDistrib = [0, 0, 7, 6, 6][self.nbPlayer]

        # Initialisation des variables du jeu
        self.resetGame()

    def resetGame(self):
        """
        Resets the game by resetting the scores and the round index, and calls resetManche().
        """

        # Scores des joueurs
        for joueur in self.listPlayer:
            joueur.setScore(0)

        # État de la partie
        self.indexManche = 1
        self.isGameOver = False

        self.resetManche()

    def resetManche(self):
        """
        Resets the round by distributing the dominoes, finding the first piece, and initializing the game board.

        Raises:
            IndexError: If the pioche list is empty.
        """

        # Distribution des dominoes
        self.distribDominoes()

        # Tant qu'il y a une serie on redistribue (les series ne peuvent arriver que dans le mode 2 joueurs
        while self.verifSeries() and self.nbPlayer == 2:
            self.distribDominoes()

        # Recherche du plus grand double
        maxPiece: (int, PieceDomino, PlayerDomino) = None
        for joueur in self.listPlayer:
            for piece in joueur.getMainJoueur():
                if piece.getFirstValue() == piece.getLastValue() and (
                        (maxPiece is None) or (piece.getSum() > maxPiece[0])):
                    maxPiece = (piece.getSum(), piece, joueur)

        # Si aucun double, on cherche juste la plus grande piece
        for joueur in self.listPlayer:
            for piece in joueur.getMainJoueur():
                if (maxPiece is None) or (piece.getSum() > maxPiece[0]):
                    maxPiece = (piece.getSum(), piece, joueur)

        # On enlève cette pièce de la main de son propriétaire
        maxPiece[2].removePieceFromHand(maxPiece[1])

        self.indexPremierJoueur = self.listPlayer.index(maxPiece[2])

        # Initialisation du plateau
        self.plateau: List[PieceDomino] = [maxPiece[1]]
        self.indexTour = 1
        self.isMancheOver = False

        self.resetTurn()

    def resetTurn(self):
        """
        Resets the turn by resetting the current player index and the turn status.

        Args:
            self: The instance of the DominoGame class.

        Returns:
            None
        """
        self.indexJoueurTour = 1
        self.isTourOver = False
        self.nbPass = 0

    def distribDominoes(self):
        """
        Distributes the domino pieces to each player.

        Raises:
            IndexError: If the pioche list is empty.

        """
        # Création de la pioche
        self.pioche = copy.deepcopy(self.listPiece)
        random.shuffle(self.pioche)

        # Vidage des mains
        for joueur in self.listPlayer:
            joueur.emptyMainJoueur()

        # Pioche des dominos
        for _, joueur in product(range(self.nbPiecesDistrib), self.listPlayer):
            joueur.appendMainJoueur(self.pioche.pop(0))

    def verifSeries(self):
        """
        Checks if there is a series of domino pieces in the players' hands.

        Returns:
            bool: True if there is a series, False otherwise.

        """
        isSerie = False
        for joueur in self.listPlayer:
            for seriePossible in set(joueur.getMainJoueur()[0].getValues()):
                for piece in joueur.getMainJoueur()[1:]:
                    if not piece.contains(seriePossible):
                        break
                else:
                    isSerie = True
                    break
            if isSerie:
                break

        return isSerie

    def playGame(self):
        """
        Plays the game until it is over.

        Args:
            self: The instance of the DominoGame class.

        Returns:
            None
        """
        self.resetGame()

        if self.display:
            print("***** Lancement de la partie *****")
            print("Liste des joueurs :")
            for joueur in self.listPlayer:
                print(f"\t- {joueur.getName()}")

        while not self.isGameOver:
            self.playManche()

        classement = self.listPlayer.copy()
        classement.sort(key=lambda x: x.getScore())

        if self.display:
            print("\nFin de la partie !")

            print(f"Le joueur {classement[0].getName()} a gagné avec {classement[0].getScore()} points")

            print("\nClassement complet :")
            for joueur in classement:
                print(f"\t- Joueur {joueur.getName()} : {joueur.getScore()} points")

    def playManche(self):
        """
        Plays a round of the game.

        Args:
            self: The instance of the DominoGame class.

        Returns:
            None
        """
        self.resetManche()

        if self.display:
            print(f"\n===== Début de la manche {self.indexManche} =====")
            print(f"Le joueur {self.listPlayer[self.indexPremierJoueur].getName()} a la plus grande "
                  f"pièce : {self.plateau[0].toString()}")

        while not self.isMancheOver and not self.isGameOver:

            self.playTurn()

            if self.nbPass == self.nbPlayer:
                self.isMancheOver = True
                if self.display:
                    print("Partie bloqué, aucune action possible et pioche vide.")

        # Update les scores
        self.updateScores()

        if self.display:
            print(f"\nScores à la fin de la manche {self.indexManche} :")
            for joueur in self.listPlayer:
                print(f"\t- Joueur {joueur.getName()} : {joueur.getScore()}/{self.scoreMax} points")
            print(f"\n===== Fin de la manche {self.indexManche} =====")

        self.indexManche += 1

    def playTurn(self):
        """
        Plays a turn of the game.

        Args:
            self: The instance of the DominoGame class.

        Returns:
            None
        """
        self.resetTurn()

        if self.display:
            print(f"\n_____ Début du tour {self.indexTour} _____")

        while not self.isTourOver and not self.isMancheOver and not self.isGameOver:
            joueurActuel = self.listPlayer[(self.indexPremierJoueur + self.indexJoueurTour) % self.nbPlayer]

            self.playTurnJoueur(joueurActuel)

            if self.indexJoueurTour > self.nbPlayer:
                self.isTourOver = True

        self.indexTour += 1

        if self.display:
            print(f"\n_____ Fin du tour {self.indexTour} _____")

    def playTurnJoueur(self, joueurActuel: PlayerDomino):
        """
        Plays a turn for a specific player.

        Args:
            joueurActuel: The PlayerDomino object representing the current player.

        Returns:
            None
        """

        if self.display:
            print(f"\nC'est au joueur {joueurActuel.getName()} de jouer")
            self.printPlateau()
            print(
                f'Main du joueur : {[f"{piece.toString()} " for piece in joueurActuel.getMainJoueur()]}'
                )

        actionPossible = self.generatePossibleAction(joueurActuel)

        # Si aucune action n'est possible, le joueur pioche
        if len(actionPossible) == 0:

            # S’il reste des dominos dans la pioche, le joueur en prend un
            if len(self.pioche) > 0:
                joueurActuel.appendMainJoueur(self.pioche.pop(0))
                if self.display:
                    print(f"Aucune action possible, le joueur {joueurActuel.getName()} à pioché la pièce "
                          f"{joueurActuel.getMainJoueur()[-1].toString()}")

            else:
                # On compte le nombre de joueur qui ont passé leur tour
                self.nbPass += 1
                if self.display:
                    print(f"Aucune action possible et la pioche est vide, le joueur {joueurActuel.getName()} passe son "
                          f"tour")
        # Sinon, il choisit une action parmis les actions disponibles
        else:
            if len(actionPossible) == 1:
                actionJoueur = actionPossible[0]
            else:
                actionJoueur = joueurActuel.chooseAction(self.plateau,
                                                         len(self.pioche),
                                                         [len(joueur.getMainJoueur()) for joueur in self.listPlayer],
                                                         actionPossible)

            if self.display:
                print(f"Le joueur {joueurActuel.getName()} a choisi l'action {actionJoueur.toString()}")

            self.computeAction(actionJoueur, joueurActuel)

            if len(joueurActuel.getMainJoueur()) == 0:
                self.isMancheOver = True

                if self.display:
                    print(f"Le joueur {joueurActuel.getName()} a posé sa dernière pièce !")

        self.indexJoueurTour += 1

    def generatePossibleAction(self, joueurActuel) -> List[ActionDomino]:
        """
        Generates a list of possible actions for the current player.

        Args:
            joueurActuel: The current player.

        Returns:
            List[ActionDomino]: A list of possible actions.

        """

        possibleAction = []
        for piece in joueurActuel.getMainJoueur():
            indexValue = piece.getIndex() * 2
            # Si la pièce peut être posée à gauche, on ajoute l'action
            if piece.contains(self.plateau[0].getFirstValue()):
                possibleAction.append(ActionDomino(indexValue, (piece, 'G')))

            # Si la pièce peut être posée à droite, on ajoute l'action
            if piece.contains(self.plateau[-1].getLastValue()):
                possibleAction.append(ActionDomino(indexValue + 1, (piece, 'D')))

        return possibleAction

    def computeAction(self, actionJoueur: ActionDomino, joueurActuel: PlayerDomino):
        """
        Computes the action chosen by the player and updates the game state accordingly.

        Args:
            actionJoueur: The ActionDomino object representing the chosen action.
            joueurActuel: The PlayerDomino object representing the current player.

        Raises:
            ActionNotValidError: If the chosen action is not valid.

        Returns:
            None
        """
        pieceJouer = actionJoueur.getPieceSideValue()[0]
        # Si on veut jouer à gauche
        if actionJoueur.pieceSideValue[1] == 'G':
            if self.plateau[0].getFirstValue() == pieceJouer.getLastValue():
                self.plateau.insert(0, pieceJouer)
            elif self.plateau[0].getFirstValue() == pieceJouer.getFirstValue():
                pieceJouer.flipPiece()
                self.plateau.insert(0, pieceJouer)
            else:
                raise ActionNotValidError(actionJoueur)

        elif self.plateau[-1].getLastValue() == pieceJouer.getFirstValue():
            self.plateau.append(pieceJouer)
        elif self.plateau[-1].getLastValue() == pieceJouer.getLastValue():
            pieceJouer.flipPiece()
            self.plateau.append(pieceJouer)
        else:
            raise ActionNotValidError(actionJoueur)

        # On retire la pièce de la main du joueur
        joueurActuel.removePieceFromHand(pieceJouer)

    def updateScores(self):
        """
        Updates the scores of the players based on the sum of the values of their remaining domino pieces.
        If a player's score reaches or exceeds the maximum score, the game is marked as over.

        Args:
            self: The instance of the DominoGame class.

        Returns:
            None
        """
        for joueur in self.listPlayer:
            joueur.addScore(
                sum(
                    piece.getSum()
                    for piece in joueur.getMainJoueur()
                    )
                )
            if joueur.getScore() >= self.scoreMax:
                self.isGameOver = True

    def printPlateau(self):
        """
        Prints the current game board.
        """
        print(f'Plateau : {[f"{piece.toString()} " for piece in self.plateau]}')


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

    def __init__(self, action: ActionDomino, message="Impossible action"):
        self.action = action
        self.message = message
        super().__init__(self.message)


class PlayersListError(Exception):
    """
    Exception raised for an invalid list of players.

    Args:
        message: The error message (default: "Invalid list of players").
    """

    def __init__(self, message="Invalid list of players"):
        self.message = message
        super().__init__(self.message)