from typing import List, Tuple

from dominoObjectOrientedVersion.actionDomino import ActionDomino
from dominoObjectOrientedVersion.dominoGame import DominoGame, PlayersListError
from dominoObjectOrientedVersion.pieceDomino import PieceDomino
from dominoObjectOrientedVersion.playerdomino import PlayerDomino


class DominoGameAI(DominoGame):
    def __init__(self, listOpponent: List[PlayerDomino], display=False, seed: int = None):

        self.nbPlayer = len(listOpponent) + 1
        if self.nbPlayer not in {2, 3, 4}:
            raise PlayersListError("Number of player opponent must be 1,2 or 3")

        self.listOpponent = listOpponent

        self.agentAi = PlayerDomino("AI-TrainingAgent")

        # L'agent est le dernier de la liste de joueurs
        listPlayer = listOpponent + [self.agentAi]

        super().__init__(listPlayer=listPlayer, seed=seed, display=display)

        self.resetTraining()

    def resetTraining(self):
        """
        Resets the game for training purposes.

        Args:
            self: The instance of the DominoGameAI class.

        Returns:
            None
        """
        self.resetGame()

        if self.display:
            print(f"\n***** Initialisation de la manche d'entrainement *****")
            print(f"Le joueur {self.listPlayer[self.indexPremierJoueur].getName()} a la plus grande "
                  f"pièce : {self.plateau[0].toString()}")

        # On avance dans la partie jusqu'à ce que ça soit à l'agent de jouer et qu'il ai un choix à faire:
        joueurActuel = self.listPlayer[(self.indexPremierJoueur + self.indexJoueurTour) % self.nbPlayer]
        self.currentPossibleAction = self.generatePossibleAction(self.agentAi)

        while (joueurActuel != self.agentAi or len(self.currentPossibleAction) == 0) and not self.isMancheOver:
            self.playTurnJoueur(joueurActuel)

            joueurActuel = self.listPlayer[(self.indexPremierJoueur + self.indexJoueurTour) % self.nbPlayer]
            self.currentPossibleAction = self.generatePossibleAction(self.agentAi)

        if self.display:
            print(f"\n***** Initialisation terminée, c'est au tour de l'agent *****")

    def getPossibleAction(self) -> List[ActionDomino]:
        return self.currentPossibleAction

    def getPlateau(self) -> List[PieceDomino]:
        return self.plateau

    def getPioche(self) -> List[PieceDomino]:
        return self.pioche

    def getTailleMainAdverse(self) -> List[int]:
        return [len(player.getMainJoueur()) for player in self.listOpponent]

    def playStep(self, action) -> Tuple[int, bool, int]:
        """
        Plays a step of the game for the agent.

        Args:
            action: The chosen action by the agent.

        Returns:
            Tuple[int, bool, int]: A tuple containing the reward, a boolean indicating if the round is over,
            and the agent's ranking in the round.
        """
        # On compte les passage pendant un tour (en partant de l'agent comme premier joueur)
        self.nbPass = 0

        reward = 0
        classementAgent = -1

        if self.display:
            print("===== Début du tour de l'agent =====")
            self.printPlateau()
            print(f"Main de l'agent : {[f'{piece.toString()} ' for piece in self.agentAi.getMainJoueur()]}")
            print(f"Le joueur {self.agentAi.getName()} a choisi l'action {action.toString()}")

        # Si l'action est illégale, on arrête l'entrainement et on lui donne une grosse pénalité.
        # Normalement, on s'est assuré en amont que l'agent choisissait parmis les actions disponibles
        if action not in self.currentPossibleAction:
            self.isMancheOver = True
            reward = -100
        else:
            # Sinon, on joue l'action de l'agent
            self.computeAction(action, self.agentAi)

            # Si l'agent a posé sa dernière pièce, alors on compte les points
            if len(self.agentAi.getMainJoueur()) == 0:
                self.isMancheOver = True

            # Sinon on continue le tour jusqu'a ce que ça soit a l'agent de jouer ou que la manche soit fini
            else:
                self.indexJoueurTour += 1

                # Actualisation du joueur actuel
                joueurActuel = self.listPlayer[(self.indexPremierJoueur + self.indexJoueurTour) % self.nbPlayer]
                self.currentPossibleAction = self.generatePossibleAction(self.agentAi)

                while ((joueurActuel != self.agentAi or len(self.currentPossibleAction) == 0)
                       and not self.isMancheOver):
                    self.playTurnJoueur(joueurActuel)

                    if self.nbPass >= self.nbPlayer:
                        self.isMancheOver = True
                        if self.display:
                            print("Partie bloqué, aucune action possible et pioche vide.")

                    joueurActuel = self.listPlayer[(self.indexPremierJoueur + self.indexJoueurTour) % self.nbPlayer]
                    self.currentPossibleAction = self.generatePossibleAction(self.agentAi)

        # Si la partie est terminé, on donne une récompense si l'agent à gagné
        if self.isMancheOver:
            self.updateScores()

            classement = self.listPlayer.copy()
            classement.sort(key=lambda x: x.getScore())

            classementAgent = classement.index(self.agentAi) + 1

            if self.display:
                print("\n***** Fin de la manche d'entrainement *****")
                print("\nClassement complet :")
                for joueur in classement:
                    print(f"\t- Joueur {joueur.getName()} : {joueur.getScore()} points")

            # Si l'agent gagne alors
            if classement[0] == self.agentAi:
                reward = 100
            # Si l'agent est dernier et donc perd, on lui donne une pénalité de 100 points
            elif classement[-1] == self.agentAi:
                reward = -100
            # Cas où l'agent est avant-dernier, on lui donne une pénalité de 50 points
            elif classement[-2] == self.agentAi:
                reward = -50
            # Cas où l'agent est 2ème sur 4
            else:
                reward = 50

        return reward, self.isMancheOver, classementAgent
