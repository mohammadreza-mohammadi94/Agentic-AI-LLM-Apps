import gradio as gr
from accounts import Account, get_share_price

account = None

def create_account(username, initial_deposit):
    global account
    account = Account(username, float(initial_deposit))
    return f'Account created for {username} with initial deposit of {initial_deposit}'

def deposit(amount):
    if account:
        account.deposit(float(amount))
        return f'Deposited: {amount}. New balance: {account.balance}'
    return "Error: No account found."

def withdraw(amount):
    if account:
        try:
            account.withdraw(float(amount))
            return f'Withdrew: {amount}. New balance: {account.balance}'
        except ValueError as e:
            return str(e)
    return "Error: No account found."

def buy_shares(symbol, quantity):
    if account:
        try:
            account.buy_shares(symbol, int(quantity))
            return f'Bought {quantity} of {symbol}. New balance: {account.balance}'
        except ValueError as e:
            return str(e)
    return "Error: No account found."

def sell_shares(symbol, quantity):
    if account:
        try:
            account.sell_shares(symbol, int(quantity))
            return f'Sold {quantity} of {symbol}. New balance: {account.balance}'
        except ValueError as e:
            return str(e)
    return "Error: No account found."

def portfolio_value():
    if account:
        return f'Total portfolio value: {account.get_portfolio_value()}'
    return "Error: No account found."

def profit_loss():
    if account:
        return f'Profit/Loss: {account.get_profit_or_loss()}'
    return "Error: No account found."

def holdings():
    if account:
        return f'Current holdings: {account.get_holdings()}'
    return "Error: No account found."

def transactions():
    if account:
        return f'Transactions: {account.get_transactions()}'
    return "Error: No account found."

with gr.Blocks() as demo:
    gr.Markdown("## Trading Simulation Platform")
    username = gr.Textbox(label="Username")
    initial_deposit = gr.Number(label="Initial Deposit", value=1000)
    create_button = gr.Button("Create Account")
    
    create_button.click(create_account, inputs=[username, initial_deposit], outputs="text")
    
    with gr.Row():
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
    
    deposit_button.click(deposit, inputs=deposit_amount, outputs="text")
    withdraw_button.click(withdraw, inputs=withdraw_amount, outputs="text")
    
    with gr.Row():
        buy_symbol = gr.Textbox(label="Buy Symbol (AAPL/TSLA/GOOGL)")
        buy_quantity = gr.Number(label="Buy Quantity")
        buy_button = gr.Button("Buy Shares")
        
        sell_symbol = gr.Textbox(label="Sell Symbol (AAPL/TSLA/GOOGL)")
        sell_quantity = gr.Number(label="Sell Quantity")
        sell_button = gr.Button("Sell Shares")

    buy_button.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs="text")
    sell_button.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs="text")
    
    value_button = gr.Button("Total Portfolio Value")
    profit_loss_button = gr.Button("Profit/Loss")
    holdings_button = gr.Button("Current Holdings")
    transactions_button = gr.Button("Transactions")

    value_button.click(portfolio_value, outputs="text")
    profit_loss_button.click(profit_loss, outputs="text")
    holdings_button.click(holdings, outputs="text")
    transactions_button.click(transactions, outputs="text")

demo.launch()