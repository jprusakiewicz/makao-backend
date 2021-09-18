import unittest

from app.card import Color, Card, Figure
from app.game import Game


class TestGame(unittest.TestCase):
    def test_calling_collor(self):
        # given
        game = Game(2)
        collor_call = "Hearts"
        # when
        game.handle_ace(collor_call)
        # then
        self.assertEqual(Color.Hearts, game.color_call)  # add assertion here

    def test_getting_call(self):
        # given
        game = Game(2)
        collor_call = "Hearts"
        game.color_call = Color(collor_call)
        # when
        call = game.get_call()
        # then
        self.assertEqual(collor_call, call)  # add assertion here

    def test_placing_card(self):
        # given
        card_to_pick = Card.to_code(Figure.Jack, Color.Hearts)
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick], 'functional': {"call": {"figure": "Ace"}}})
        self.assertEqual(game.pile[0], Card.to_code(Figure.Jack, Color.Hearts))

    def test_figure_call_positive_simple(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Jack, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Ace, Color.Spades)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick], 'functional': {"call": {"figure": "Ace"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2], 'functional': {"call": {"color": "Spades"}}})
        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.figure_call, None)
        self.assertEqual(game.color_call, Color.Spades)

    def test_figure_call_negative_simple(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Jack, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Spades)
        # when
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick], 'functional': {"call": {"figure": "Ace"}}})

        self.assertEqual(game.figure_call, Figure.Ace)  # precondition
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn), {'picked_cards': [card_to_pick2]})
        # then
        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(Figure.Ace, game.figure_call)
        self.assertEqual(None, game.color_call)

    def test_color_call_placing_card(self):
        # Negative case- you cannot put Five-Clubs on top of Ace-Spades
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick1 = Card.to_code(Figure.Ace, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Clubs)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick1
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick1],
                                        'functional': {"call": {"color": "Spades"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})
        self.assertEqual(game.pile[0], card_to_pick1)

    def test_color_call_positive_simple(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Ace, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Clubs)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})
        self.assertEqual(game.pile[0], card_to_pick2)

    def test_color_call_negative_simple(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Ace, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Diamonds)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})
        self.assertEqual(game.pile[0], card_to_pick)
        self.assertEqual(Color.Clubs, game.color_call)
        self.assertEqual(None, game.figure_call)

    def test_color_call_queen_wrong_color(self):
        # negative test- cannot put any queen when specific color is called
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Ace, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Queen, Color.Diamonds)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})
        self.assertNotEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pile[0], card_to_pick)

    def test_color_call_queen_right_color(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Ace, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Queen, Color.Clubs)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})
        self.assertEqual(game.pile[0], card_to_pick2)

    def test_picking_two(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Two, Color.Spades)
        expected_pick_count = 2

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})

        self.assertEqual(game.pile[0], card_to_pick)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_double_two(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Two, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Two, Color.Clubs)

        expected_pick_count = 4

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_two_three_same_color(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Two, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Three, Color.Spades)

        expected_pick_count = 5

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_two_three_another_color(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Two, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Three, Color.Diamonds)

        expected_pick_count = 5

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_three_two_same_color(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Three, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Two, Color.Spades)

        expected_pick_count = 5

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_three_two_another_color(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Three, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.Two, Color.Diamonds)

        expected_pick_count = 5

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)


if __name__ == '__main__':
    unittest.main()
