from typing import List, Tuple

from dominoGame import DominoGame
from actionDomino import ActionDomino
from pieceDomino import PieceDomino
from playerdomino import PlayerDomino


class PlayerDominoHumain(PlayerDomino):

    def __init__(self, name="Bob", *args, **kwargs) -> None:
        name = f"{name} [H]"
        super().__init__(name, *args, **kwargs)

    def chooseAction(
            self, plateau: List[PieceDomino], taillePioche: int,
            tailleMainAdverse: List[int], possibleAction: List[ActionDomino]
            ) -> ActionDomino:

        # Affichage des actions possibles
        print("Actions possible :")
        for index, action in enumerate(possibleAction):
            print(f"\t- {index} : {action.toString()} [{action.getIndexValue()}]")

        indexAction = int(input("Choisissez une action : "))

        while indexAction not in range(len(possibleAction)):
            indexAction = int(input("Action impossible, veuillez choisir un action valide : "))

        return possibleAction[indexAction]
