from typing import Tuple


class PieceDomino:
    """
    Represents a domino piece.

    Args:
        listValues: The tuple of values on the piece.

    Methods:
        isInPiece: Checks if a value is present on the piece.
        getValues: Returns the tuple of values on the piece.
        flipPiece: Reverses the order of the values on the piece.
        getFirstValue: Returns the first value on the piece.
        getLastValue: Returns the last value on the piece.

    Returns:
        bool: True if the value is present on the piece, False otherwise.
        Tuple[int]: The tuple of values on the piece.
        int: The first value on the piece.
        int: The last value on the piece.
    """

    def __init__(self, values: Tuple[int], index: int):
        self.values = values
        self.index = index

    def contains(self, value: int) -> bool:
        return value in self.values

    def getValues(self) -> Tuple[int]:
        return self.values

    def getSum(self) -> int:
        return sum(self.values)

    def flipPiece(self):
        self.values = self.values[::-1]

    def getFirstValue(self) -> int:
        return self.values[0]

    def getLastValue(self) -> int:
        return self.values[-1]

    def getIndex(self) -> int:
        return self.index

    def toString(self) -> str:
        return f"|{self.getFirstValue()}|{self.getLastValue()}|"