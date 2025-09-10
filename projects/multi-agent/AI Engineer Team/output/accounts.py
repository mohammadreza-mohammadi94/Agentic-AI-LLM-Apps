class Account:
    def __init__(self, username: str, initial_deposit: float):
        self.username = username
        self.balance = initial_deposit
        self.portfolio = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float):
        self.balance += amount
        self.transactions.append(f'Deposited: {amount}')

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError('Insufficient funds to withdraw')
        self.balance -= amount
        self.transactions.append(f'Withdrew: {amount}')

    def buy_shares(self, symbol: str, quantity: int):
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.balance:
            raise ValueError('Cannot afford this purchase')
        self.balance -= total_cost
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity
        self.transactions.append(f'Bought {quantity} of {symbol}')

    def sell_shares(self, symbol: str, quantity: int):
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise ValueError('Not enough shares to sell')
        price = get_share_price(symbol)
        total_revenue = price * quantity
        self.balance += total_revenue
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.transactions.append(f'Sold {quantity} of {symbol}')

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.portfolio.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.portfolio

    def get_transactions(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    if symbol == "AAPL":
        return 150.0
    elif symbol == "TSLA":
        return 720.0
    elif symbol == "GOOGL":
        return 2800.0
    else:
        raise ValueError("Unknown stock symbol")