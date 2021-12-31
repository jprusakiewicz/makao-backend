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
        self.assertEqual(game.pile[0], card_to_pick)

    def test_negative_placing_three_on_ten(self):
        # given
        card_on_pile = Card.to_code(Figure.Ten, Color.Spades)
        card_to_pick = Card.to_code(Figure.Three, Color.Hearts)
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick], 'functional': {"call": {"figure": "Ace"}}})
        self.assertNotEqual(game.pile[0], card_to_pick)

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
        # when
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick1
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick1],
                                        'functional': {"call": {"color": "Spades"}}})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})
        # then
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
        self.assertEqual(game.color_call, None)

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
                                       {'picked_cards': [card_to_pick]})

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
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_double_king_negative(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.King, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.King, Color.Clubs)

        expected_pick_count = 5

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_double_king_positive(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.King, Color.Spades)
        card_to_pick2 = Card.to_code(Figure.King, Color.Clubs)

        expected_pick_count = 1

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick]})

        # pick cards 5
        game.handle_players_other_move(str(game.person_turn),
                                       {'other_move': {"type": "pick_new_card"}})

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
                                       {'picked_cards': [card_to_pick]})
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
                                       {'picked_cards': [card_to_pick]})
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
                                       {'picked_cards': [card_to_pick]})
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
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_five_diamonds_on_king_clubs(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.King, Color.Clubs)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Diamonds)

        expected_pick_count = 1

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_five_clubs_on_king_clubs(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.King, Color.Clubs)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Clubs)

        expected_pick_count = 1

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_five_heart_on_king_heart(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.King, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Hearts)

        expected_pick_count_first = 5
        expected_pick_count_second = 1

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick)
        self.assertEqual(game.pick_count, expected_pick_count_first)

        # pick cards 5
        game.handle_players_other_move(str(game.person_turn),
                                       {'other_move': {"type": "pick_new_card"}})
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count_second)

    def test_picking_king_diamond_on_king_heart(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.King, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.King, Color.Diamonds)

        expected_pick_count_first = 5
        expected_pick_count_second = 1

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick)
        self.assertEqual(game.pick_count, expected_pick_count_first)

        # pick 5 cards
        game.handle_players_other_move(str(game.person_turn),
                                       {'other_move': {"type": "pick_new_card"}})
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(expected_pick_count_second, game.pick_count)

    def test_picking_king_spade_on_king_heart(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.King, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.King, Color.Spades)

        expected_pick_count = 5

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick]})
        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick)
        self.assertEqual(game.pick_count, expected_pick_count)

        # pick 5 cards
        game.handle_players_other_move(str(game.person_turn),
                                       {'other_move': {"type": "pick_new_card"}})
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2]})

        self.assertEqual(game.pile[0], card_to_pick2)
        self.assertEqual(game.pick_count, expected_pick_count)

    def test_picking_joker_five_spades_on_six_spades(self):
        # given
        card_on_pile = Card.to_code(Figure.Six, Color.Spades)
        card_to_pick = Card.to_code(Figure.Joker, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Spades)

        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        self.assertEqual(card_to_pick, game.pile[0])

    def test_picking_joker_five_clubs_on_six_spades_negative(self):
        # given
        card_on_pile = Card.to_code(Figure.Six, Color.Spades)
        card_to_pick = Card.to_code(Figure.Joker, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Clubs)

        # when
        game = Game(2)
        game.pile = [card_on_pile]
        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_on_pile, game.pile[0])

    def test_picking_joker_five_clubs_on_ace_calling_clubs_positive(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Ace, Color.Spades)
        card_to_pick = Card.to_code(Figure.Joker, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Clubs)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0],
                                        'functional': {"call": {"color": "Clubs"}}})

        self.assertEqual(card_to_pick0, game.pile[0])

        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2
        # doesnt pass. passes if you delete joker
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(card_to_pick2, game.pile[1])

    def test_picking_joker_five_clubs_on_ace_calling_clubs_negative(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Ace, Color.Spades)
        card_to_pick = Card.to_code(Figure.Joker, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0],
                                        'functional': {"call": {"color": "Clubs"}}})

        self.assertEqual(card_to_pick0, game.pile[0])

        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2
        # doesnt pass. passes if you delete joker
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick0, game.pile[0])

    def test_picking_joker_four_clubs_on_four_diamonds(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Four, Color.Diamonds)
        card_to_pick = Card.to_code(Figure.Joker, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Four, Color.Clubs)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0]})

        self.assertEqual(card_to_pick0, game.pile[0])

        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2
        # doesnt pass. passes if you delete joker
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(card_to_pick2, game.pile[1])

    def test_picking_joker_hearts_four_clubs_on_four_diamonds(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Four, Color.Diamonds)
        card_to_pick = Card.to_code(Figure.Joker, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Four, Color.Clubs)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0]})

        self.assertEqual(card_to_pick0, game.pile[0])

        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2
        # doesnt pass. passes if you delete joker
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(card_to_pick2, game.pile[1])

    def test_picking_joker_hearts_five_diamonds_on_four_diamonds_negative(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Four, Color.Diamonds)
        card_to_pick = Card.to_code(Figure.Joker, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Diamonds)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0]})

        self.assertEqual(card_to_pick0, game.pile[0])

        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2

        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick0, game.pile[0])

    def test_picking_joker_five_clubs_on_jack_calling_five(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Jack, Color.Clubs)
        card_to_pick = Card.to_code(Figure.Joker, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Five, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0],
                                        'functional': {"call": {"figure": "Five"}}})

        self.assertEqual(card_to_pick0, game.pile[0])

        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2

        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(card_to_pick2, game.pile[1])

    def test_picking_joker_five_clubs_on_jack_calling_five_negative(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Jack, Color.Clubs)
        card_to_pick = Card.to_code(Figure.Joker, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Six, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0],
                                        'functional': {"call": {"figure": "Five"}}})

        self.assertEqual(card_to_pick0, game.pile[0])

        game.players[str(game.person_turn)][0] = card_to_pick
        game.players[str(game.person_turn)][1] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick]})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick0, game.pile[0])

    def test_raising_ace(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Ace, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Ace, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"color": "Clubs"}}})

        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(game.color_call, Color.Clubs)

        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2],
                                        'functional': {"call": {"color": "Diamonds"}}})

        # then
        self.assertEqual(card_to_pick2, game.pile[0])
        self.assertEqual(game.color_call, Color.Diamonds)

    def test_raising_jack(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Jack, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Jack, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"figure": "Six"}}})

        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(game.figure_call, Figure.Six)

        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2],
                                        'functional': {"call": {"figure": "Five"}}})

        # then
        self.assertEqual(card_to_pick2, game.pile[0])
        self.assertEqual(game.figure_call, Figure.Five)

    def test_raising_jack_negative(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick = Card.to_code(Figure.Jack, Color.Diamonds)
        card_to_pick2 = Card.to_code(Figure.Ace, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick],
                                        'functional': {"call": {"figure": "Six"}}})

        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(game.figure_call, Figure.Six)

        game.players[str(game.person_turn)][0] = card_to_pick2
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2],
                                        'functional': {"call": {"color": "Five"}}})

        # then
        self.assertEqual(card_to_pick, game.pile[0])
        self.assertEqual(game.figure_call, Figure.Six)

    def test_picking_joker_raising_jack(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Jack, Color.Diamonds)
        card_to_pick1 = Card.to_code(Figure.Joker, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Jack, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0],
                                        'functional': {"call": {"figure": "Six"}}})

        self.assertEqual(card_to_pick0, game.pile[0])
        self.assertEqual(game.figure_call, Figure.Six)

        game.players[str(game.person_turn)][0] = card_to_pick1
        game.players[str(game.person_turn)][1] = card_to_pick2

        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick1],
                                        'functional': {"call": {"figure": "Five"}}})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick1, game.pile[0])
        self.assertEqual(card_to_pick2, game.pile[1])
        self.assertEqual(game.figure_call, Figure.Five)

    def test_picking_joker_raising_ace(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Ace, Color.Diamonds)
        card_to_pick1 = Card.to_code(Figure.Joker, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Ace, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0],
                                        'functional': {"call": {"color": "Diamonds"}}})

        self.assertEqual(card_to_pick0, game.pile[0])
        self.assertEqual(Color.Diamonds, game.color_call)

        game.players[str(game.person_turn)][0] = card_to_pick1
        game.players[str(game.person_turn)][1] = card_to_pick2

        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick1],
                                        'functional': {"call": {"color": "Clubs"}}})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick1, game.pile[0])
        self.assertEqual(card_to_pick2, game.pile[1])
        self.assertEqual(Color.Clubs, game.color_call)

    def test_picking_joker_raising_ace_negative(self):
        # given
        card_on_pile = Card.to_code(Figure.Queen, Color.Spades)
        card_to_pick0 = Card.to_code(Figure.Ace, Color.Diamonds)
        card_to_pick1 = Card.to_code(Figure.Joker, Color.Hearts)
        card_to_pick2 = Card.to_code(Figure.Jack, Color.Spades)

        # when
        game = Game(2)
        game.pile = [card_on_pile]

        game.players[str(game.person_turn)][0] = card_to_pick0
        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick0],
                                        'functional': {"call": {"color": "Diamonds"}}})

        self.assertEqual(card_to_pick0, game.pile[0])
        self.assertEqual(game.color_call, Color.Diamonds)

        game.players[str(game.person_turn)][0] = card_to_pick1
        game.players[str(game.person_turn)][1] = card_to_pick2

        game.handle_players_cards_move(str(game.person_turn),
                                       {'picked_cards': [card_to_pick2, card_to_pick1],
                                        'functional': {"call": {"figure": "Five"}}})  # idx 0 card + idx 1 joker

        # then
        self.assertEqual(card_to_pick0, game.pile[0])
        self.assertEqual(game.color_call, Color.Diamonds)


if __name__ == '__main__':
    unittest.main()
