from .players import Players, TheHouse, Coin, coins
from .player import Player, Deck, Card
from .views import Menu
import os
import time


class Game21:
    players: Players = Players()
    house: TheHouse = TheHouse()
    menu: Menu = Menu()
    deck: Deck = Deck()
    round: int = 0

    def __init__(self) -> None:
        self.run()

    def run(self) -> None:
        self.menu.animation_wait(1.5)
        self.menu.show_menu()
        self.menu.show_start_options()
        start_game: str = input("select: ").strip().lower()
        if start_game == "q":
            exit()
        else:
            print("Vamos a jugar!")
            self.create_players()
            while True:
                self.ask_play_round()
                if self.check_for_players():
                    if self.round == 0:
                        self.crupier_init_game()
                    while any(
                        player.status == "play_round" and player.score < 21
                        for player in Players.players_list
                    ):
                        self.menu.clear_screen()
                        for player in Players.players_list:
                            player.status = (
                                "BlackJack!"
                                if player.score == 21 and self.round == 0
                                else player.status
                            )
                            player.status = (
                                "Lose!" if player.score > 21 else player.status
                            )
                            if player.status == "play_round" and player.score < 21:
                                # Acciones específicas por jugador
                                self.player_play(player=player)
                            else:
                                pass
                        self.round += 1
                    self.crupier_end_game()
                    new_round = input("Volver a comenzar?")
                    if new_round.lower() in ["s", "y", "si", "yes"]:
                        self.reset_game()
                        status_players = ", ".join(
                            f"({playe_r.name} - {playe_r.status} - {playe_r.score})"
                            for playe_r in self.players.players_list
                        )
                        input(status_players)
                    else:
                        break
                else:
                    print("No hay jugadores para la ronda")
                    print("Reiniciando la ronda.")
                    time.sleep(1)

    def ask_play_round(self) -> None:
        # entrar a la partida
        for player in self.players.players_list:
            self.menu.clear_screen()
            print("Iniciar la apuesta, costo 2 fichas")
            print(player.name.center(20, "*"))
            if len(player.chips) <= 0:
                print(f"{player.name}, no tienes fichas!, comprate unas")
                player.status = "buying_chips"
                while player.status == "buying_chips":
                    self.house.sale_chips(player=player)
            in_to_round = input(
                f"\n{player.name}, ¿Quieres entrar a la partida? (si/no): "
            )
            if in_to_round.lower() in ["s", "si", "yes", "y"]:
                player.status = "play_round"
                print(f"El jugador: {player.name} entra a la ronda.")
                if len(player.chips) == 1:
                    coin_color = player.chips[0][0].color
                else:
                    print("Cuales fichas quieres apostar? ")
                    print("\nInventario: \n")
                    print("\tColor\tCantidad\n")
                    for coin in player.chips:
                        print(f"\t{coin[0].color}\t{coin[1]}")
                    print("")
                    coin_color: str = input("\ntipo de fichas: ").strip()
                selected_coin: Coin = next(
                    (
                        coin
                        for coin in coins
                        if coin.color.lower() == coin_color.lower()
                    ),
                    None,
                )  # Efficient coin selection
                # Apuesta de dos fichas
                how_many_chips: int = 2
                player.chip_bet = selected_coin.color
                player.update_coins(selected_coin, quantity=-how_many_chips)
                print(f"Se apuestan de 2 fichas {selected_coin.color}")
                new_card: Card = self.deck.deal_card()
                player.add_card_to_hand(new_card)
            else:
                player.status = "no_play_round"
                input("No se contesto afirmativamente, el jugador no entra en la ronda")

    def check_for_players(self) -> None:
        return any(player.status == "play_round" for player in Players.players_list)

    def player_play(self, player: Player = None) -> None:
        # Comenzar la partida
        # se repartes dos cartas por jugador y 2 para el dealer(Crupier)
        player.calculate_score_hand()
        print(
            f"\nRonda: {self.round} Turno de: {" ".join(player.name.center(20, "*"))}\n"
        )
        if self.round == 0:
            user_selection = "1"
        else:
            self.players.show_players_info()
            self.menu.show_cards_game(
                house=self.house, players=self.players, round=self.round
            )
            user_selection = self.menu.user_options(player_name=player.name)
        if user_selection in ["1", "2", "3", "4"]:
            if user_selection == "1":
                new_card: Card = self.deck.deal_card()
                new_card.is_as(player.score, round=self.round)
                player.add_card_to_hand(new_card)
                player.calculate_score_hand()
            if user_selection == "2":
                player.status = "stand"
            if user_selection == "2":
                player.status = "quit"
            if user_selection == "2":
                player.status = "safe"
        else:
            return self.player_play(player)

    def buy_chips(self) -> None:
        for player in self.players.players_list:
            while True:
                print(f"Jugador {player.name}")
                self.house.sale_chips(player=player)
                self.players.show_players_info()
                if player.status != "buying_chips":
                    break

    def create_players(self, num_players=None) -> None:
        try:
            if num_players is None:
                num_players: int = int(input("Cuantos jugadores(as)?: "))
                if num_players > 6:
                    input("El Numero maximo de jugadores es 5, vuelve a elejir!")
                    self.menu.clear_screen()
                    return self.create_players(num_players=None)
        except:
            return self.create_players(num_players=1)
        try:
            if 0 < num_players < 6:
                for _ in range(num_players):
                    print()
                    name: str = " ".join(
                        input(f"Nombre del jugador {_ + 1}?: ").rsplit()
                    )
                    wallet: int = 10000  # cantidad inicial en $
                    if name:
                        self.players.create_new_player(((name, wallet),))
                    else:
                        # Nombre generico
                        self.players.create_new_player(((f"player_{_ + 1}", wallet),))

        except Exception as e:
            input(f"No se introduzco una valor válido: {str(e)}")
            return self.create_players()
        finally:
            print("\n")

    def is_winner(self, crupier_score, player_score) -> tuple[bool, str, int]:
        if player_score == 21 and crupier_score < 21:
            return True, "BlackJack!", 5
        elif (
            player_score <= 21 and crupier_score <= 21 and player_score == crupier_score
        ):
            return True, "Draw!", 2
        elif player_score <= 21 and (
            crupier_score > 21 or player_score > crupier_score
        ):
            return True, "Winner!", 4
        elif player_score > 21:
            return False, "Lose!", 0
        else:
            return False, "No result!", 0  # Para casos no contemplados

    def crupier_end_game(self) -> None:
        self.menu.clear_screen()
        self.menu.show_cards_game(
            house=self.house, players=self.players, round=self.round
        )
        for crupier in self.house.players_list:
            crupier.hand_card[0].hide = False  # Mostrar al carta escondida
            # Revisar si hay un AS en la mano del crupier y mostar las cartas
            self.menu.display_player_hand(player=crupier)  # mostrar cartas
            for card in crupier.hand_card:  # iniciar el loop de cartas
                card.is_as(crupier.score, round=self.round)  # Revisar si es un AS
            crupier.calculate_score_hand()
            # --Loop para finalizar las partidas hasta obtener hasta 17 maximo
            while crupier.score <= 17:
                new_card: Card = self.deck.deal_card()
                new_card.is_as(crupier.score, round=self.round)
                crupier.add_card_to_hand(new_card)
                self.round += 1
                self.menu.animation_wait(0.6)
                crupier.calculate_score_hand()
                crupier_score_num: int = crupier.score
            self.menu.show_cards_game(
                house=self.house, players=self.players, round=self.round
            )
            for player in self.players.players_list:
                reward, status, reward_chips = self.is_winner(
                    player_score=player.score, crupier_score=crupier_score_num
                )
                print(f"Jugador: {player.name}, {reward}, {status}, {player.chip_bet} - {reward_chips}")
                input()

    def crupier_init_game(self) -> None:
        print("Iniciando mesa =>")
        self.menu.animation_wait(2.3)
        for crupier in self.house.players_list:
            print("Obteniendo Cartas Iniciales")
            new_card: Card = self.deck.deal_card()
            hide_card: Card = self.deck.deal_card()
            hide_card.hide_unhide_card()
            crupier.add_card_to_hand(card=hide_card)
            crupier.add_card_to_hand(card=new_card)

    def reset_game(self) -> None:
        self.round = 0
        self.deck.reset_deck()
        self.players.reset_hand_and_score()
        self.house.reset_hand_and_score()
