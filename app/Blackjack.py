import random

class Blackjack:
    def __init__(self, num_players):
        self.deck = self.create_deck()
        self.players = {f"Player {i+1}": [] for i in range(num_players)}
        self.dealer = []
    
    def create_deck(self):
        """Crear y barajar la baraja"""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck
    
    def deal_card(self, hand):
        """Repartir una carta a una mano"""
        hand.append(self.deck.pop())
    
    def calculate_points(self, hand):
        """Calcular puntos de una mano"""
        points = 0
        aces = 0
        for card in hand:
            if card['rank'].isdigit():
                points += int(card['rank'])
            elif card['rank'] in ['J', 'Q', 'K']:
                points += 10
            else:
                aces += 1
        
        # Contar los Ases como 1 u 11
        for _ in range(aces):
            if points + 11 <= 21:
                points += 11
            else:
                points += 1
        return points
    
    def play(self):
        """Jugar una ronda de Blackjack"""
        # Repartir cartas iniciales
        for player in self.players:
            self.deal_card(self.players[player])
            self.deal_card(self.players[player])
        self.deal_card(self.dealer)
        self.deal_card(self.dealer)
        
        # Turnos de los jugadores
        for player in self.players:
            while True:
                print(f"{player} tiene {self.players[player]} (Puntos: {self.calculate_points(self.players[player])})")
                action = input("¿Qué quieres hacer? (P: Pedir, T: Plantarte): ").upper()
                if action == 'P':
                    self.deal_card(self.players[player])
                    if self.calculate_points(self.players[player]) > 21:
                        print(f"{player} se pasó de 21. ¡Pierde!")
                        break
                elif action == 'T':
                    break
        
        # Turno del crupier
        print(f"El crupier tiene {self.dealer}")
        while self.calculate_points(self.dealer) < 17:
            self.deal_card(self.dealer)
            print(f"El crupier pide carta. Ahora tiene {self.dealer}")
        
        dealer_points = self.calculate_points(self.dealer)
        print(f"El crupier tiene {self.dealer} (Puntos: {dealer_points})")
        
        # Determinar resultados
        for player in self.players:
            player_points = self.calculate_points(self.players[player])
            if player_points > 21:
                print(f"{player} pierde.")
            elif dealer_points > 21 or player_points > dealer_points:
                print(f"{player} gana.")
            elif player_points == dealer_points:
                print(f"{player} empata con el crupier.")
            else:
                print(f"{player} pierde.")

# Ejemplo de uso
juego = Blackjack(num_players=2)
juego.play()
