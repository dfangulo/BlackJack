from ..player import Player
from ..coin import *

import random


class Players:
    players_list: list[Player] = []

    def create_new_player(self, players: list = []) -> None:
        try:
            for player in players:
                new_player: Player = Player(name=player[0], wallet_founds=player[1])
                self.players_list.append(new_player)
        except:
            pass

    def show_players_info(self) -> None:
        print("-" * 100)
        print(f'{"Jugador".center(50)} {"Bolsa".center(20)} {"Fichas".center(15)}')
        for player in self.players_list:
            if player.chips:
                for i, chip in enumerate(player.chips):
                    if i == 0:
                        print(
                            f"{player.name.ljust(45)}{f'$ {player.return_wallet_funds():,.2f}':>20}{f'{chip[0].color}:{chip[1]: >5}'.rjust(20)}"
                        )
                    else:
                        print(
                            f"{' '.ljust(65)}{f'{chip[0].color}:{chip[1]: >5}'.rjust(20)}"
                        )
            else:
                print(
                    f"{player.name.ljust(45)}{f'$ {player.return_wallet_funds():,.2f}':>20}\n"
                )
        print("-" * 100)
        # input("Enter para continuar! ...".rjust(100))

    def delete_player_by_index(self, index: int) -> bool:
        """Elimina un jugador de la lista dado su índice."""
        try:
            if 0 <= index < len(self.players_list):
                removed_player = self.players_list.pop(index)
                print(f"Jugador eliminado: {removed_player.name}")
                return True
            else:
                print("Índice fuera de rango.")
                return False
        except Exception as e:
            print(f"Error al eliminar jugador: {e}")
            return False

    def shuffle_players(self) -> None:
        """Baraja la lista de jugadores en un orden aleatorio."""
        random.shuffle(self.players_list)
        print("La lista de jugadores ha sido mezclada aleatoriamente.")

    def get_player(self, index: int) -> Player:
        """Encuentra y devuelve un jugador de la lista dado su índice."""
        try:
            if 0 <= index < len(self.players_list):
                return self.players_list[index]
            else:
                print("Índice fuera de rango.")
                return None
        except Exception as e:
            print(f"Error al obtener jugador: {e}")
            return None

    def reset_hand_and_score(self)->None:
        for player in self.players_list:
            player.hand_card = []
            player.status = "reset"
            player.score_hand()
            
class TheHouse(Players):
    players_list: list[Player] = []

    def __init__(self):
        super().__init__()
        self.create_new_player((("Crupie", 1000000),))

    def pay(self, player: Player, amount) -> bool:
        if player.deposit_wallet(amount=amount):
            self.players_list[0].charge_wallet(amount)
            print(f"\tSe hizo un deposito a {player.player_name()}, por: {amount}")
            return True

    def charge(self, player: Player, amount) -> bool:
        if player.charge_wallet(amount=amount):
            self.players_list[0].deposit_wallet(amount)
            print(f"\tSe hizo un cobro a {player.player_name()}, por: {amount}")
            return True

    def sale_chips(self,player: Player) -> None:
        print("Venta de Fichas\n")
        print("Costos:")
        for coin in coins:
            print(f"{coin.color}, Costo: ${coin.value:,.2f}")
        print("\nQ para salir")
        print("\n")
        to_pay: int = 0

        try:
            coin_color: str = input("tipo de fichas: ").strip()
            selected_coin: Coin = next(
                (coin for coin in coins if coin.color.lower() == coin_color.lower()),
                None,
            )  # Efficient coin selection
            if coin_color.lower() == "q":
                print("No se compraron mas fichas")
                player.status = "play"
                return             

            if selected_coin is None:
                print("No se encontró una ficha con ese color.")
                player.status = "buying_chips"
                return

            chips_quantity = int(input("Cuantas fichas: ").strip())
            to_pay = chips_quantity * selected_coin.value

            if self.charge(player=player, amount=to_pay):
                player.update_coins(
                    selected_coin, chips_quantity
                )  # Add new coin if not found
                print(
                    f"\t{player.name.capitalize()}, se agregaron {chips_quantity} fichas {coin_color}'s tu inventario.\n"
                )
                if player.return_wallet_funds() > 1:
                    continue_buying = input("Desea seguir comprando fichas? (s)")
                    if continue_buying.lower() in ["s", "y", "si", "yes"]:
                        player.status = "buying_chips"
                else:
                    player.status = "play"
                return
            else:
                player.status = "play"
                input("No hay fondos para pagar las fichas!")
        except Exception as e:
            print(f"Error: {str(e)}")
            return self.sale_chips(player=player)  # Optionally retry on error

