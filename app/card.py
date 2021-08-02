from enum import Enum


class Color(Enum):
    Spades = "Spades"
    Hearts = "Hearts"
    Diamonds = "Diamonds"
    Clubs = "Clubs"


class Figure(Enum):
    Ace = "Ace"
    Two = "Two"
    Three = "Three"
    Four = "Four"
    Five = "Five"
    Six = "Six"
    Seven = "Seven"
    Eight = "Eight"
    Nine = "Nine"
    Ten = "Ten"
    Jack = "Jack"
    # Four = "Knight"
    Queen = "Queen"
    King = "King"
    Joker = "Joker"


FUNCTIONAL_FIGURES = [Figure.Ace, Figure.Two, Figure.Three, Figure.Four, Figure.Jack, Figure.Queen, Figure.Joker,
                      Figure.King]


class Card:
    def __init__(self, figure: Figure, color: Color):
        self.code: str = Card.get_code(figure, color)
        self.color: Color = color
        self.figure: Figure = figure

    @staticmethod
    def get_code(figure: Figure, color: Color) -> str:
        code = "U+F0"

        if color is Color.Spades:
            code += "A"
        elif color is Color.Hearts:
            code += "B"
        elif color is Color.Diamonds:
            code += "C"
        elif color is Color.Clubs:
            code += "D"

        if figure is Figure.Ace:
            code += "1"
        elif figure is Figure.Two:
            code += "2"
        elif figure is Figure.Three:
            code += "3"
        elif figure is Figure.Four:
            code += "4"
        elif figure is Figure.Five:
            code += "5"
        elif figure is Figure.Six:
            code += "6"
        elif figure is Figure.Seven:
            code += "7"
        elif figure is Figure.Eight:
            code += "8"
        elif figure is Figure.Nine:
            code += "9"
        elif figure is Figure.Ten:
            code += "A"
        elif figure is Figure.Jack:
            code += "B"
        elif figure is Figure.Queen:
            code += "D"
        elif figure is Figure.King:
            code += "E"
        elif figure is Figure.Joker:
            code += "F"

        return code

    def is_functional(self):
        if self.figure in FUNCTIONAL_FIGURES:
            return True
        return False
