from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
import config

client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)
account = dict(client.get_account())
for k, v in account.items():
    print(f"{k:30}{v}")
    
order_details = MarketOrderRequest(
    symbol = "SPY",
    qty = 1, # number of shares
    side = OrderSide.BUY,
    time_in_force = TimeInForce.DAY,
)

order = client.submit_order(order_data=order_details)
trades = TradingStream(config.API_KEY, config.SECRET_KEY, paper=True)

#define an asynchronous function as this is a websocket API: advanced technology that makes it possible to open a two-way interactive communication session between the user's browser and a server. With this API, you can send messages to a server and receive event-driven responses without having to poll the server for a reply.
async def trade_status(data):
    print(data)
    
trades.subscribe_trade_updates(trade_status)
trades.run()

assets = [asset for asset in client.get_all_positions()]#get an object for each asset
positions = [(asset.symbol, asset.qty, asset.current_price) for asset in assets]
print("Positions")
print(f"{'Symbol':9}{'Qty':>4}{'Value':>15}") # this is some terminal string maipulation shit just use docstrings
print('-'*28)
for position in positions:
    print(f"{position[0]:9}{position[1]:>4}{float(position[1]) * float(position[2]):>15.2f}")


client.close_all_positions(cancel_orders=True) # sells all positions

