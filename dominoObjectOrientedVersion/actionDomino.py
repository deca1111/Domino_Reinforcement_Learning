from typing import Tuple
from pieceDomino import PieceDomino


class ActionDomino:
    """
    Represents an action in a domino game.

    Args:
        indexValue: The index value of the action.
        pieceSideValue: The piece side value of the action.

    Methods:
        getIndexValue: Returns the index value of the action.
        getPieceSideValue: Returns the piece side value of the action.

    Returns:
        int: The index value of the action.
        Tuple[PieceDomino, chr]: The piece side value of the action.
    """

    def __init__(self, indexValue: int, pieceSideValue: Tuple[PieceDomino, chr]):
        self.indexValue = indexValue
        self.pieceSideValue = pieceSideValue

    def getIndexValue(self) -> int:
        return self.indexValue

    def getPieceSideValue(self) -> Tuple[PieceDomino, chr]:
        return self.pieceSideValue

    def toString(self) -> str:
        return (f"|{self.pieceSideValue[0].getFirstValue()}|{self.pieceSideValue[0].getLastValue()}| à "
                f"{'Gauche' if self.pieceSideValue[1]=='G' else 'Droite'}")
