from ...player import Player
from ...players import Players
import os
import time


class Menu:
    def __init__(self):
        pass

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def show_menu(self) -> None:
        self.clear_screen()
        print("\n" * 4, "Black Jack!".center(80), "\n" * 2)

    def show_start_options(self) -> str:
        print(
            """
            1 => Iniciar Juego (enter)
            2 => Agregar Jugadores
            3 => Comprar monedas
            4 => Cambiar monedas
            5 => Eliminar Jugador
            6 => Salir Juego 
            """
        )
        answer = input("Seleccione una opción: ").strip().lower()
        if answer == "1":
            return "Iniciar Juego"
        elif answer == "2":
            return "Agregar Jugadores"
        elif answer == "3":
            return "Comprar monedas"
        elif answer == "4":
            return "Cambiar monedas"
        elif answer == "5":
            return "Eliminar Jugador"
        elif answer == "6":
            return "Salir Juego"
        

    def user_options(self, player: Player, round: int = 0) -> str:
        print(
            f"""
{" ".join(player.name.center(40, "*"))}
    Ronda: {round}
              
              1 => Pedir Cartas
              2 => Plantarse
              3 => Retirarse
              4 => Seguro
              
              Puntos: {player.score}
              
              """
        )
        self.display_player_hand(player)
        return input(f"{player.name} Selección: ").lower().strip()

    def show_cards_game(self, house: Players, players: Players, round: int = 0) -> None:
        print(f"Ronda [{round}]\n")
        for crupier in house.players_list:
            crupier.calculate_score_hand()
            print(f"\tCartas de la mesa puntuacion {crupier.score}: ")
            self.display_player_hand(crupier)
        for player in players.players_list:
            player.calculate_score_hand()
            # Asegúrate de definir cómo obtener el color del objeto Coin
            formatted_chips = ", ".join(
                f"({coin.color}, {value})" for coin, value in player.chips
            )
            print(
                f"\tCartas {player.name} Puntuación {player.score}, fichas restantes: [{formatted_chips}]:"
            )
            self.display_player_hand(player)

    def display_player_hand(self, player: Player):
        """Displays the player's hand with a custom separator."""
        time.sleep(0.3)
        hand_cards = [str(card) for card in player.hand_card]
        print(" ".join(hand_cards).center(60, "☆").center(80, "-"))
        print("\n")

    def animation_wait(
        self, time_sleep: float = 0.1, many_chars: int = 3, char: str = "."
    ):
        """
        Muestra una animación de puntos durante el tiempo especificado.

        Args:
            time (int): Número de segundos que durará la animación.
        """

        for _ in range(
            many_chars
        ):  # Ajusta el número de iteraciones para controlar la velocidad
            print(f"{char}", end="", flush=True)
            time.sleep(
                time_sleep / many_chars
            )  # Pausa de 0.1 segundos entre cada punto

        print()  # Salto de línea al finalizar
