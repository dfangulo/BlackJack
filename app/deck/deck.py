#from .card import Card
from app.deck.card import Card
import random


class Deck:
    def __init__(self):
        self.deck_init()

    def deck_init(self) -> None:
        """Crea un mazo estándar de 52 cartas."""
        self.cards: list[Card] = [
            Card(value=value, suit=suit, score=min(value, 10))
            for suit in ["Corazones", "Diamantes", "Picas", "Tréboles"]
            for value in range(1, 14)
        ]
        random.shuffle(self.cards)

    def deal_card(self):
        """Reparte una carta del mazo."""
        if self.cards:
            card: Card = self.cards.pop()
            return card
        else:
            print("El mazo está vacío.")
            return None

    def reset_deck(self):
        """Reinicia el mazo y lo baraja."""
        self.deck_init()


if __name__ == "__main__":
    new_deck: Deck = Deck()
    count: int = 0
    while len(new_deck.cards) > 0:
        count += 1
        card = new_deck.deal_card()
        print(card, count)
