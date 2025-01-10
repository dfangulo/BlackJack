import datetime
class Wallet:
    def __init__(self, player_name, funds):
        self.wallet = player_name
        self.total_funds = funds
        self.history = {"creation": funds}
        self.history["transactions"] = []  # Initialize a list to store transactions


    def __str__(self):
        return f"A nombre de: {self.wallet}, {self.money_format(self.total_funds)}"

    def return_funds(self) -> int:
        return self.total_funds

    def charge(self, amount) -> int:
        # ...
        timestamp = datetime.datetime.now()
        self.history["transactions"].append({"type": "charge", "amount": amount, "timestamp": timestamp})
        self.total_funds -= amount

    def deposit(self, amount) -> int:
        # ...
        timestamp = datetime.datetime.now()
        self.history["transactions"].append({"type": "deposit", "amount": amount, "timestamp": timestamp})
        self.total_funds += amount
        

    def money_format(self, amount) -> str:
        return f"${amount:,.2f}"

    def get_transactions_by_type(self, transaction_type):
        return [transaction for transaction in self.history["transactions"] if transaction["type"] == transaction_type]

    def get_balance_at(self, timestamp):
        balance = self.history["creation"]
        for transaction in self.history["transactions"]:
            if transaction["timestamp"] <= timestamp:
                if transaction["type"] == "charge":
                    balance -= transaction["amount"]
                else:
                    balance += transaction["amount"]
        return balance

if __name__ == "__main__":
    new_wallet: Wallet = Wallet(player_name="David Angulo", funds=1000000)
    new_wallet.charge(amount=500000)
    new_wallet.deposit(1000000)
    new_wallet.charge(amount=500000)
    new_wallet.deposit(1000000)
    new_wallet.charge(amount=500000)
    new_wallet.deposit(1000000)
    charges = new_wallet.get_transactions_by_type("charge")
    for charge in charges:
        print(charge)