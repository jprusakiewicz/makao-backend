import unittest

from app.deck import Deck


class TestDeck(unittest.TestCase):
    def test_creating_deck(self):
        deck = Deck(2)
        self.assertIsInstance(deck, Deck)

    def test_getting_all_cards(self):
        deck = Deck.set_full_deck()
        list_length = len(deck)
        self.assertIsInstance(deck, list)
        self.assertEqual(list_length, 55)

    def test_getting_new_game_cards(self):
        deck = Deck(2)
        new_game = deck.get_new_game_cards(2)
        print(new_game)
        self.assertIsInstance(new_game["players"], dict)


if __name__ == '__main__':
    unittest.main()
