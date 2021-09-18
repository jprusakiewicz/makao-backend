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
    Queen = "Queen"
    King = "King"
    Joker = "Joker"


FUNCTIONAL_FIGURES = [Figure.Ace, Figure.Two, Figure.Three, Figure.Four, Figure.Jack, Figure.Queen, Figure.Joker,
                      Figure.King]

FUNCTIONAL_FIGURES_WITH_CALL = [Figure.Ace, Figure.Jack]


class Card:
    def __init__(self, figure: Figure, color: Color):
        self.code: str = Card.to_code(figure, color)
        self.color: Color = color
        self.figure: Figure = figure

    @staticmethod
    def from_code(code: str) -> 'Card':
        figure = Card.get_figure_from_code(code)
        color = Card.get_color_from_code(code)
        card = Card(figure=figure, color=color)
        return card

    @staticmethod
    def to_code(figure: Figure, color: Color) -> str:
        code = "U+1F0"

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

    @staticmethod
    def get_color(letter: str, color=None) -> Color:
        if len(letter) > 1:
            raise ValueError
        letter = letter.upper()

        if letter == "A":
            color = Color.Spades
        elif letter == "B":
            color = Color.Hearts
        elif letter == "C":
            color = Color.Diamonds
        elif letter == "D":
            color = Color.Clubs
        return color

    @staticmethod
    def get_figure(letter: str, figure=None) -> Figure:
        if len(letter) > 1:
            raise ValueError
        letter = letter.upper()

        if letter == "1":
            figure = Figure.Ace
        elif letter == "2":
            figure = Figure.Two
        elif letter == "3":
            figure = Figure.Three
        elif letter == "4":
            figure = Figure.Four
        elif letter == "5":
            figure = Figure.Five
        elif letter == "6":
            figure = Figure.Six
        elif letter == "7":
            figure = Figure.Seven
        elif letter == "8":
            figure = Figure.Eight
        elif letter == "9":
            figure = Figure.Nine
        elif letter == "A":
            figure = Figure.Ten
        elif letter == "B":
            figure = Figure.Jack
        elif letter == "D":
            figure = Figure.Queen
        elif letter == "E":
            figure = Figure.King
        elif letter == "F":
            figure = Figure.Joker

        return figure

    def is_functional(self):
        if self.figure in FUNCTIONAL_FIGURES:
            return True
        return False

    @staticmethod
    def get_figure_from_code(code) -> Figure:
        figure = Card.get_figure(code[-1])
        return figure

    @staticmethod
    def get_color_from_code(code) -> Color:
        color = Card.get_color(code[-2])
        return color

    def is_functional_with_call(self):
        if self.figure in FUNCTIONAL_FIGURES_WITH_CALL:
            return True
        return False
