import time
class Card:

    def __init__(self, value: str, suit: str, score: int, hide: bool = False):
        self.value: str = value
        self.suit: str = suit
        self.score: int = score
        self.hide: bool = hide
        # Diccionario para los palos
        self.card_suit: dict = {
            "Picas": "A",
            "Corazones": "B",
            "Diamantes": "C",
            "Tréboles": "D",
        }
        self.card_suit_icon: dict = {
            "Picas": "2660",
            "Corazones": "2665",
            "Diamantes": "2666",
            "Tréboles": "2663",
        }

        # Diccionario para los valores especiales
        self.special_values: dict = {
            10: "A",  # 10
            11: "B",  # J
            12: "C",  # Q
            13: "D",  # K
        }
        self.special_values_names: dict = {
            1: "A",  # AS
            10: "10",  # 10
            11: "J",  # J
            12: "Q",  # Q
            13: "K",  # K
        }

    def __str__(self) -> str:
        if self.hide:
            return f"[{chr(int("1F0A0", 16))} : ---] "
        return f"[{self.print_card()} : {self.name_card()}] "

    def is_as(self, total_score, round) -> str:
        try:
            if self.score == 1:
                self.score = 11 if total_score + 11 <= 21 and round == 0 else self.score
        except:
            pass

    def print_card(self) -> str:
        base: str = f"1F0{self.card_suit[self.suit]}"
        if 1 <= self.value <= 9:
            unicode = int(base + str(self.value), 16)
        else:
            unicode = int(base + self.special_values[self.value], 16)
        return chr(unicode)

    def name_card(self) -> str:
        if 2 <= self.value <= 9:
            return f"{str(self.value).center(2)}{self.suit_icon()}"
        else:
            return (
                f"{self.special_values_names[self.value].center(2)}{self.suit_icon()}"
            )

    def suit_icon(self) -> str:
        unicode = int(self.card_suit_icon[self.suit], 16)
        return chr(unicode)

    def hide_unhide_card(self) -> None:
        self.hide = True if self.hide == False else False


if __name__ == "__main__":
    for suit in ['Picas','Corazones','Diamantes','Tréboles']:
        for value in range(1, 14):
            card: Card = Card(value=value, suit=suit, score=min(value, 10))
            # card.hide_unhide_card()
            str_card = card.print_card()
            print(card, end='\b')
        print('\n')
