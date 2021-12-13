from itertools import product
from random import shuffle
from typing import List, Union

from app.card import Card, Figure, Color


class Game:
    def __init__(self, number_of_players: int):
        self.pick_count = 1
        self.can_skip = False
        self.reverse = False
        self.call_moves_count = 0
        self.color_call: Union[None, Color] = None
        self.figure_call: Union[None, Figure] = None
        self.person_turn = 1
        self.is_blocked = False
        self.has_picked = False
        self.stack: List[Card] = self.set_full_deck()
        self.pile: List[str] = [self.get_nonfunctional_card().code]
        self.players: dict = self.get_new_game_cards(number_of_players)
        self.makaos: dict = self.set_all_players_makaos_false()
        self.used_cards: List[str] = []
        self.used_cards.extend(self.pile)

    def shuffle_deck(self):
        shuffle(self.stack)

    @staticmethod
    def set_full_deck() -> List[Card]:
        cards = []
        prod = list(product(Figure, Color))
        for p in prod:
            card = Card(p[0], p[1])
            cards.append(card)
        cards.remove(
            next(c for c in cards if c.figure == Figure.Joker and c.color == Color.Spades))
        cards.remove(
            next(c for c in cards if c.figure == Figure.Joker and c.color == Color.Clubs))
        # theres no spades and clubs joker
        shuffle(cards)
        return cards

    def get_new_game_cards(self, number_of_players: int, cards_in_hand: int = 5):
        players = {}
        if number_of_players > 4 or number_of_players <= 1:
            raise ValueError
        for player_id in range(number_of_players):
            player_cards = []
            while len(player_cards) != cards_in_hand:
                player_cards.append(self.get_card().code)
            players[str(player_id + 1)] = player_cards
        return players

    def handle_players_cards_move(self, game_id, player_move: dict):
        self.set_players_makao_false(game_id)
        picked_cards: List[str] = player_move['picked_cards']

        if self.is_card_in_players_hand(game_id, picked_cards[0]) \
                and all([self.can_put_on_pile(card) for card in picked_cards]):
            self.used_cards.append(picked_cards[0])
            self.remove_cards_from_players_hand(game_id, picked_cards[0])
            picked_cards.reverse()
            self.pile = picked_cards
            card = Card.from_code(picked_cards[0])

            if card.is_functional_with_call():
                if card.is_functional_with_call():
                    function = player_move["functional"]
                    if card.figure == Figure.Jack:
                        call_figure = function["call"]["figure"]
                        self.handle_jack(call_figure)
                    elif card.figure == Figure.Ace:
                        call_color = function["call"]["color"]
                        self.handle_ace(call_color)
            else:
                if card.figure == Figure.Two:
                    self.handle_two()
                elif card.figure == Figure.Three:
                    self.handle_three()
                elif card.figure == Figure.Four:
                    self.handle_four()
                elif card.figure == Figure.King:
                    self.handle_king(card.color)
            return True

    def handle_players_other_move(self, game_id, player_move: dict):
        other_move = player_move['other_move']
        type = other_move['type']
        if type == "pick_new_card" and self.is_blocked is False and self.has_picked == False:
            self.pick_new_card(game_id)
            self.has_picked = True
            self.can_skip = True

        elif type == "skip" and self.can_skip:
            self.is_blocked = False
            self.has_picked = False
            if self.color_call is not None or self.figure_call is not None:
                self.call_moves_count += 1
            if self.call_moves_count >= len(self.players) - 1:
                self.color_call = None
                self.figure_call = None
            return True

    def get_players_cards(self, game_id):
        return self.players[game_id]

    def handle_players_makao_call(self, game_id):
        if len(self.get_players_cards(game_id)) <= 1:
            self.makaos[game_id] = True
            return True

    def set_players_makao_false(self, game_id):
        self.makaos[game_id] = False

    def handle_makao_move(self, game_id, player_move: dict):
        makao_type = player_move['makao_move']['type']
        if makao_type == "makao" or makao_type == "finish":
            return self.handle_players_makao_call(game_id)

        elif makao_type == "nick_click":
            direction = player_move['makao_move']['direction']
            enemy_id = None

            if game_id == '1':
                if direction == "left":
                    enemy_id = '2'

                elif direction == "top":
                    enemy_id = '3'

                elif direction == "right":
                    enemy_id = '4'

            if game_id == '2':
                if direction == "left":
                    enemy_id = '3'

                elif direction == "top":
                    enemy_id = '4'

                elif direction == "right":
                    enemy_id = '1'

            if game_id == '3':
                if direction == "left":
                    enemy_id = '4'

                elif direction == "top":
                    enemy_id = '1'

                elif direction == "right":
                    enemy_id = '2'

            if game_id == '4':
                if direction == "left":
                    enemy_id = '1'

                elif direction == "top":
                    enemy_id = '2'

                elif direction == "right":
                    enemy_id = '3'

            if enemy_id is not None:
                self.handle_enemy_makao_call(enemy_id)

    def check_if_should_pick_makao_cards(self, player_id):
        player_cards = self.players[player_id]
        if len(player_cards) <= 1 and self.makaos[player_id] is False:
            return True

    def handle_enemy_makao_call(self, enemy_id):
        if self.check_if_should_pick_makao_cards(enemy_id):
            self.pick_makao_card(enemy_id)

    @staticmethod
    def set_deck(cards_in_game: List[Card]) -> List[Card]:
        all_cards = Game.set_full_deck()
        all_cards_not_in_game = []
        if not any(cards_in_game):
            return all_cards
        for card in all_cards:
            if card not in cards_in_game:
                all_cards_not_in_game.append(card)
        return all_cards_not_in_game

    def get_card(self) -> Card:
        if len(self.stack) == 0:
            self.stack.extend(map(lambda x: Card.from_code(x), self.used_cards))
            self.used_cards = []
        return self.stack.pop()

    def get_nonfunctional_card(self) -> Card:
        while Card.is_functional(self.stack[-1]):
            self.shuffle_deck()
        return self.get_card()

    def remove_players_cards(self, game_id):
        self.used_cards.extend(self.players[game_id])
        self.players[game_id] = []

    def is_card_in_players_hand(self, player_id: str, picked_card: str):
        if picked_card not in self.get_players_cards(player_id):
            return False
        return True

    def can_put_on_pile(self, picked_card: str) -> bool:
        can_put = False
        players_card = Card.from_code(picked_card)
        pile_card = Card.from_code(self.pile[-1])

        # króle
        if pile_card.figure == Figure.King and pile_card.color == Color.Spades \
                or pile_card.figure == Figure.King and pile_card.color == Color.Hearts:

            # skipping defensive kings logic.
            # if players_card.figure == Figure.King and players_card.color == Color.Diamonds \
            #         or players_card.figure == Figure.King and players_card.color == Color.Clubs \
            #         or self.pick_count == 1:
            #     can_put = True

            if self.pick_count == 1:
                can_put = True

        elif self.is_blocked is False or self.is_blocked is True and players_card.figure == Figure.Four:
            if self.pick_count > 1 and (players_card.figure == Figure.Two or players_card.figure == Figure.Three):
                can_put = True

            elif self.pick_count == 1 or pile_card.figure == Figure.Joker:
                if self.color_call is not None:
                    if self.color_call == players_card.color:
                        can_put = True
                        self.color_call = None
                        self.call_moves_count = 0
                elif self.figure_call is not None:
                    if self.figure_call == players_card.figure:
                        can_put = True
                        self.figure_call = None
                        self.call_moves_count = 0
                elif players_card.color == pile_card.color or players_card.figure == pile_card.figure \
                        or players_card.figure == Figure.Joker or players_card.figure == Figure.Queen \
                        or pile_card.figure == Figure.Queen or pile_card.figure == Figure.Joker:
                    can_put = True
                else:
                    print("can not put this card on pile")
        return can_put

    def remove_cards_from_players_hand(self, player_id: str, card: str):
        self.players[player_id].remove(card)

    def pick_makao_card(self, player_id):
        try:
            for i in range(5):
                self.players[player_id].append(self.get_card().code)
        except IndexError:
            print("no cards in stack!!!")

    def pick_new_card(self, player_id):
        try:
            for i in range(self.pick_count):
                self.players[player_id].append(self.get_card().code)
        except IndexError:
            print("no cards in stack!!!")
        self.pick_count = 1

    def reset_parameters(self):
        self.reverse = False
        self.has_picked = False
        if self.is_blocked is False:
            self.can_skip = False

    def get_current_state(self, player_id):
        rest_players = {}
        pl = self.players.copy()
        player_hand = pl[str(player_id)]
        pl.pop(str(player_id))
        for player in self.players:
            if player != player_id:
                rest_players[player] = len(self.players[player])

        if player_id == '1':
            try:
                rest_players['left'] = rest_players['4']
                del rest_players['4']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['3']
                del rest_players['3']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['2']
                del rest_players['2']
            except KeyError:
                pass

        elif player_id == '2':
            try:
                rest_players['left'] = rest_players['1']
                del rest_players['1']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['4']
                del rest_players['4']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['3']
                del rest_players['3']
            except KeyError:
                pass

        elif player_id == '3':
            try:
                rest_players['left'] = rest_players['2']
                del rest_players['2']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['1']
                del rest_players['1']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['4']
                del rest_players['4']
            except KeyError:
                pass

        if player_id == '4':
            try:
                rest_players['left'] = rest_players['3']
                del rest_players['3']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['2']
                del rest_players['2']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['1']
                del rest_players['1']
            except KeyError:
                pass

        return {
            "player_hand": player_hand,
            "rest_players": rest_players,
            "pile": self.pile}

    def get_current_watcher_state(self, player_id):
        rest_players = {}
        pl = self.players.copy()
        bottom = len(pl[str(player_id)])
        pl.pop(str(player_id))
        for player in self.players:
            if player != player_id:
                rest_players[player] = len(self.players[player])

        rest_players['bottom'] = bottom

        if player_id == '1':
            try:
                rest_players['left'] = rest_players['4']
                del rest_players['4']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['3']
                del rest_players['3']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['2']
                del rest_players['2']
            except KeyError:
                pass

        elif player_id == '2':
            try:
                rest_players['left'] = rest_players['1']
                del rest_players['1']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['4']
                del rest_players['4']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['3']
                del rest_players['3']
            except KeyError:
                pass

        elif player_id == '3':
            try:
                rest_players['left'] = rest_players['2']
                del rest_players['2']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['1']
                del rest_players['1']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['4']
                del rest_players['4']
            except KeyError:
                pass

        if player_id == '4':
            try:
                rest_players['left'] = rest_players['3']
                del rest_players['3']
            except KeyError:
                pass
            try:
                rest_players['top'] = rest_players['2']
                del rest_players['2']
            except KeyError:
                pass
            try:
                rest_players['right'] = rest_players['1']
                del rest_players['1']
            except KeyError:
                pass

        return {
            "rest_players": rest_players,
            "pile": self.pile}

    def handle_two(self):
        if self.pick_count == 1:
            self.pick_count = 2
        else:
            self.pick_count += 2

    def handle_three(self):
        if self.pick_count == 1:
            self.pick_count = 3
        else:
            self.pick_count += 3

    def handle_four(self):
        self.is_blocked = True
        self.can_skip = True

    def handle_king(self, color):
        if color == Color.Spades:
            self.pick_count = 5
            self.reverse = True
        elif color == Color.Clubs:
            self.pick_count = 1
            self.can_skip = True
        elif color == Color.Hearts:
            self.pick_count = 5
        elif color == Color.Diamonds:
            self.pick_count = 1
            self.can_skip = True

    def handle_jack(self, call_figure):
        self.figure_call = Figure(call_figure)
        print("handling jack: ", self.figure_call)

    def handle_ace(self, call_color):
        self.color_call = Color(call_color)
        print("handling ace: ", self.color_call)

    def get_call(self):
        if self.color_call:
            return self.color_call.value
        elif self.figure_call:
            return self.figure_call.value

    def set_all_players_makaos_false(self):
        makaos = {}
        for player_id in range(0, 4):
            makaos[str(player_id + 1)] = False
        return makaos
