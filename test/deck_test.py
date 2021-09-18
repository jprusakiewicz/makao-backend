import unittest

from app.game import Game


class TestDeck(unittest.TestCase):
    def test_creating_deck(self):
        deck = Game(2)
        self.assertIsInstance(deck, Game)

    def test_getting_all_cards(self):
        deck = Game.set_full_deck()
        list_length = len(deck)
        self.assertIsInstance(deck, list)
        self.assertEqual(list_length, 54)

    def test_getting_new_game_cards(self):
        deck = Game(2)
        new_game = deck.get_new_game_cards(2)
        print(new_game)
        self.assertIsInstance(new_game, dict)


if __name__ == '__main__':
    unittest.main()
