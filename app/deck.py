from itertools import product
from random import shuffle
from typing import List

from app.card import Card, Figure, Color


class Deck:
    def __init__(self, number_of_players: int):
        self.person_turn = 1
        self.stack: List[Card] = self.set_full_deck()
        self.pile = [self.get_nonfunctional_card().code]
        self.players = self.get_new_game_cards(number_of_players)
        self.used_cards = []

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
            next(c for c in cards if c.figure == Figure.Joker and c.color == Color.Spades))  # theres no spades joker
        shuffle(cards)
        return cards

    def get_new_game_cards(self, number_of_players: int):
        players = {}
        if number_of_players > 4 or number_of_players <= 1:
            raise ValueError  # todo except this
        for player_id in range(number_of_players):
            player_cards = []
            while len(player_cards) != 4:
                player_cards.append(self.get_card().code)
            players[str(player_id + 1)] = player_cards
        return players  # todo

    def handle_players_move(self, player_id, picked_cards):
        # self.validate_cards(picked_cards)
        # self.validate_picked_cards(player_id, picked_cards)

        self.used_cards.extend(picked_cards)
        for card in picked_cards:
            if card in self.players[player_id]:
                self.players[player_id].remove(card)
        self.pile = picked_cards[-1]

    @staticmethod
    def set_deck(cards_in_game: List[Card]) -> List[Card]:
        all_cards = Deck.set_full_deck()
        all_cards_not_in_game = []
        if not any(cards_in_game):
            return all_cards
        for card in all_cards:
            if card not in cards_in_game:
                all_cards_not_in_game.append(card)
        return all_cards_not_in_game

    def get_card(self) -> Card:
        return self.stack.pop()

    def get_nonfunctional_card(self) -> Card:
        while Card.is_functional(self.stack[-1]):
            self.shuffle_deck()
        return self.get_card()
