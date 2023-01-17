import alpaca_trade_api as tradeapi
# from fear_greed_index import CNNFearAndGreedIndex
import requests
import ast
from pandas import Timestamp
from dateutil import parser
import datetime


class Bot:
    def __init__(self):
        self.key = "PK692E83Q4X2KRCUGN3A"
        self.secret = "9KOKEm1duXyj3uXDCZjoEnIHzbcQCFF9tEtgpdEz"
        self.alpaca_endpoint = "https://paper-api.alpaca.markets"
        self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = "SPY"

    def test_market_order(self):
        self.api.submit_order(self.symbol, notional=200.5, side='buy', type='market', time_in_force='day')
        self.api.cancel_all_orders()
        print("submitted and canceled")

    # def example_function(self, target):  # submit_order()
    #     if self.current_order is not None:
    #         self.api.cancel_order(self.current_order.id)
    #     delta = target - self.position
    #     if delta == 0:
    #         return
    #     print(f'Processing the order for {target} shares')
    #
    #     if delta > 0:
    #         buy_quantity = delta
    #         if self.position < 0:
    #             buy_quantity = min(abs(self.position), buy_quantity)
    #         print(f'Buying {buy_quantity} shares')
    #         self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)
    #     elif delta < 0:
    #         sell_quantity = abs(delta)
    #         if self.position > 0:
    #             sell_quantity = min(abs(self.position), sell_quantity)
    #         print(f'Selling {sell_quantity} share')
    #         self.current_order = self.api.submit_order(self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)

    def adjust_positions(self, new_ratio):
        balances = self.get_account_balances()
        current_ratio = float(balances["long"]) / float(balances["equity"])
        delta = new_ratio - current_ratio
        print(f'Last ratio: {current_ratio * 100}%')
        print(f'New ratio: {new_ratio * 100}%')
        if delta == 0:
            return
        elif delta > 0:
            notional_buy_amount = delta * float(balances["equity"])
            print(f'Buying ${notional_buy_amount} worth of {self.symbol} shares')
            self.api.submit_order(self.symbol, notional=notional_buy_amount, side='buy', type='market', time_in_force='day')
        elif delta < 0:
            notional_sell_amount = abs(delta) * float(balances["equity"])
            print(f'Selling ${notional_sell_amount} worth of {self.symbol} shares')
            self.api.submit_order(self.symbol, notional=notional_sell_amount, side='sell', type='market', time_in_force='day')

        """notes: wait until market opens to check how shorting works//then decide on what model"""

    def get_account_balances(self):
        account = self.api.get_account()
        return {"equity": account.equity, "cash": account.cash, "long": account.long_market_value, "short": account.short_market_value}

    def last_order_time(self):
        return self.api.list_orders('all', 1)[0].submitted_at

    def cancel_orders(self):
        print(f'Cancelling all previous orders')
        self.api.cancel_all_orders()


class Index:
    def __init__(self):
        self.url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
        self.headers = {
            "X-RapidAPI-Key": "bbbae29cf3msh3373a446fb6309cp13f3d9jsn7eebc48a49be",
            "X-RapidAPI-Host": "fear-and-greed-index.p.rapidapi.com"
        }
        self.now = ()
        self.prev = ()
        self.week = ()
        self.month = ()
        self.year = ()
        self.last_update = ()

    def set_vals(self):
        response = requests.request("GET", self.url, headers=self.headers)
        res_dict = ast.literal_eval(response.text)
        self.now = (res_dict["fgi"]["now"]["value"], res_dict["fgi"]["now"]["valueText"])
        self.prev = (res_dict["fgi"]["previousClose"]["value"], res_dict["fgi"]["previousClose"]["valueText"])
        self.week = (res_dict["fgi"]["oneWeekAgo"]["value"], res_dict["fgi"]["oneWeekAgo"]["valueText"])
        self.month = (res_dict["fgi"]["oneMonthAgo"]["value"], res_dict["fgi"]["oneMonthAgo"]["valueText"])
        self.year = (res_dict["fgi"]["oneYearAgo"]["value"], res_dict["fgi"]["oneYearAgo"]["valueText"])
        self.last_update = (res_dict['lastUpdated']['epochUnixSeconds'], res_dict['lastUpdated']['humanDate'])

    def get_vals(self):
        return {"now": self.now, "prev": self.prev, "week": self.week, "month": self.month, "year": self.year, "last_update": self.last_update}


def positions_updated(index, trade_bot):
    fg_time = parser.parse(index.last_update[1])
    order_time = trade_bot.last_order_time()
    return order_time >= fg_time


def algorithm():
    fg_index = Index()
    fg_index.set_vals()
    fg_dict = fg_index.get_vals()
    bot = Bot()
    print(f'Last Fear and Greed Index Update: {parser.parse(fg_index.last_update[1])}')
    if positions_updated(fg_index, bot):
        print(f'All orders are up to date')
        return
    if bot.api.list_orders():
        bot.cancel_orders()
    new_ratio = fg_dict["now"][0] / 100
    bot.adjust_positions(new_ratio)


if __name__ == "__main__":
    algorithm()
