import unittest

from app.card import Card, Color, Figure


class TestCards(unittest.TestCase):
    def test_setting_up_card(self):
        card = Card(Figure.Ace, Color.Spades)
        self.assertIsInstance(card, Card)

    def test_checking_is_functional(self):
        functional_card = Card(Figure.Ace, Color.Spades)
        not_functional_card = Card(Figure.Six, Color.Spades)
        self.assertEqual(functional_card.is_functional(), True)
        self.assertEqual(not_functional_card.is_functional(), False)


if __name__ == '__main__':
    unittest.main()
