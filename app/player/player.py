from ..wallet import Wallet
from ..deck import Card
from ..coin import *


class Player:
    def __init__(self, name, wallet_founds: int = 0):
        self.name: str = name
        self.wallet: Wallet = Wallet(player_name=name, funds=wallet_founds)
        self.hand_card: list[Card] = []
        self.score: int = 0
        self.status: str = "play_round"
        self.reward: bool = False
        self.chip_bet:str = "color"
        self.chips: list[(Coin, int),] = []

    def player_name(self) -> str:
        return f"Jugador: {self.name}"

    def return_wallet_funds(self) -> int:
        return self.wallet.return_funds()

    def charge_wallet(self, amount) -> None:
        if amount <= self.wallet.return_funds():
            self.wallet.charge(amount)
            return True

    def deposit_wallet(self, amount) -> None:
        self.wallet.deposit(amount)
        return True

    def add_card_to_hand(self, card: Card) -> None:
        self.hand_card.append(card)

    def calculate_score_hand(self) -> None:
        self.score = 0
        for card in self.hand_card:
            self.score += card.score if card.hide == False else self.score

    def update_coins(self, coin: Coin, quantity, status:str = None) -> None:
        """Actualiza la cantidad de una ficha existente o agrega una nueva.

        Args:
            coin: Coin(value, color) - La ficha a actualizar o agregar.
            quantity: int - La cantidad de fichas a agregar.
        """
        # Buscamos si la ficha ya existe en el inventario
        for i, (existing_coin, existing_quantity) in enumerate(self.chips):
            if existing_coin == coin:
                # Si encontramos la ficha, actualizamos la cantidad
                self.chips[i] = (coin, existing_quantity + quantity)
                return
        # Si no encontramos la ficha, la agregamos
        self.chips.append((coin, quantity))
        self.status = status
