class Coin:
    def __init__(self, value, color):
        self.value: int = value
        self.color: str = color


blanca = Coin(1, "Blanca")
roja = Coin(5, "Roja")
azul = Coin(10, "Azul")
verde = Coin(25, "Verde")
naranja = Coin(50, "Naranja")
negra = Coin(100, "Negra")
purpura = Coin(500, "Púrpura")
dorada = Coin(1000, "Dorada")

coins: list[Coin] = [
    blanca,
    roja,
    azul,
    verde,
    naranja,
    negra,
    purpura,
    dorada,
]
if __name__=='__main__':
    for coin in coins:
        print(f"{coin.color}, ${coin.value:,.2f}")
"""
Valores monedas:

1 unidad: Representada con fichas blancas o de colores similares.
5 unidades: Fichas de color rojo (común en Estados Unidos).
10 unidades: A menudo son fichas azules o grises.
Valor medio:

25 unidades: Verde.
50 unidades: Naranja o colores personalizados según el casino.
Alto valor:

100 unidades: Negro.
500 unidades: Púrpura o rosa.
1,000 unidades: Amarillo o dorado.
"""
