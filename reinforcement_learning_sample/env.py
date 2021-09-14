from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import math


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


class CryptoSingleEnv(Env):  # Fit one particular coin first
    def __init__(self, df):
        self.leverage = 2
        # Training / Validation dataset
        self.df = df
        self.dp_coin = 3
        self.dp_usdt = 8
        # Actions we can take: buy long (0-100%), sell long(0-100%), hold long (), buy short (0-100%), sell short(0-100%), hold short()
        # Dimensions are defined as: [Long action(0:buy,1:sell,2:hold), Long percentage(0-100%), short action, short percentage].
        # Percentage is defined as: amount of available balance (when buy), will multiply with leverage afterwards. Amount of total opened positions (when sell). Ignore when hold.
        self.action_space = Box(
            low=np.array([[0, 0, 0, 0]]), high=[3, 1, 3, 1], dtype=np.float16
        )
        # [Open,High,Low,Close,Volume (USDT),tradecount,fundingrate,...(append balancestate)...] (add RSI, MACD, multiple tokens later?)
        self.observation_space = Box(
            low=np.array([0, 0, 0, 0, 0, 0, -1]),  # ,0,0,0,0,0,0,0,0,np.NINF]),
            high=np.array(
                [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 1]
            ),  # np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]),
        )
        # [Total Balance, Available balance, Long position (amt), long margin, long avg entry price, Short position (amt), short margin,short avg entry, sharpe_ratio]
        self.state = np.array([10000, 10000, 0, 0, 0, 0, 0, 0, 0])
        self.timestamp = df["timestamp"].values[0]
        self.endtime = df["timestamp"].values[-1]
        self.pastbal = [10000]
        self.pastroi = []
        self.starttime = self.timestamp

    def step(self, action):
        # check liquidate condition and update balance
        self.timestamp += 60000  # 1 minute currently
        latest_data = self.df.loc[self.df["timestamp"] == self.timestamp].values
        funding_time = latest_data[7]
        funding_rate = latest_data[6]
        open_price = latest_data[0]
        pnl_long = (open_price - self.state[4]) * self.state[2]
        if pnl_long < 0 and self.state[3] + pnl_long <= 0:
            self.state[3] = 0
            self.state[2] = 0
            pnl_long = 0
        pnl_short = (self.state[7] - open_price) * self.state[5]
        if pnl_short < 0 and self.state[6] + pnl_short <= 0:
            self.state[5] = 0
            self.state[6] = 0
            pnl_short = 0
        self.state[0] = (
            self.state[1] + self.state[3] + self.state[6] + pnl_long + pnl_short
        )
        if funding_time == self.timestamp:  # It's funding time!
            net_position = self.state[2] - self.state[5]
            funding = net_position * open_price * funding_rate
            self.state[1] -= funding
            self.state[0] -= funding
        # Apply action
        if action[0] // 1 == 0:  # Buy long
            if action[1] >= 98:
                action[1] = 100
            elif action[1] <= 2:
                action[1] = 0
            amount_to_buy = min(
                self.state[1],
                round_up(self.state[1] * action[1] * self.leverage, self.dp_usdt),
            )  # in USDT
            amount_coin = round_down((amount_to_buy / open_price), self.dp_coin)
            if amount_coin > 0:
                self.state[1] -= amount_to_buy / self.leverage
                self.state[4] = (self.state[4] * self.state[2] + amount_to_buy) / (
                    self.state[2] + amount_coin
                )
                self.state[2] += amount_coin
                self.state[3] += amount_to_buy / self.leverage
        elif action[0] // 1 == 1:  # sELL LONG
            if action[1] >= 98:
                action[1] = 100
            elif action[1] <= 2:
                action[1] = 0
            amount_to_sell = min(
                self.state[2], round_up(self.state[2] * action[1], self.dp_coin)
            )  # in target coin
            if amount_to_sell > 0:
                return_leverage = round_up(self.state[3] * action[1], self.dp_usdt)
                pnl = (open_price - self.state[4]) * amount_to_sell
                self.state[3] -= return_leverage
                self.state[3] = max(0, self.state[3])
                self.state[2] -= amount_to_sell
                self.state[1] += return_leverage + pnl
        if action[2] // 1 == 0:  # SHORT Sell
            if action[3] >= 98:
                action[3] = 100
            elif action[3] <= 2:
                action[3] = 0
            amount_to_buy = min(
                self.state[1],
                round_up(self.state[1] * action[3] * self.leverage, self.dp_usdt),
            )  # in USDT
            amount_coin = round_down((amount_to_buy / open_price), self.dp_coin)
            if amount_coin > 0:
                self.state[1] -= amount_to_buy / self.leverage
                self.state[7] = (self.state[7] * self.state[5] + amount_to_buy) / (
                    self.state[5] + amount_coin
                )
                self.state[5] += amount_coin
                self.state[6] += amount_to_buy / self.leverage
        elif action[2] // 1 == 1:  # short buy
            if action[3] >= 98:
                action[3] = 100
            elif action[3] <= 2:
                action[3] = 0
            amount_to_sell = min(
                self.state[5], round_up(self.state[5] * action[3], self.dp_coin)
            )  # in target coin
            if amount_to_sell > 0:
                return_leverage = round_up(self.state[6] * action[3], self.dp_usdt)
                pnl = (self.state[7] - open_price) * amount_to_sell
                self.state[6] -= return_leverage
                self.state[6] = max(0, self.state[6])
                self.state[5] -= amount_to_sell
                self.state[1] += return_leverage + pnl
        else:
            pass

        # # Calculate reward
        # daily roi% + current time multiplied by weight, then calculate mean and variance
        latest_roi = (self.state[0] - self.pastbal[-1]) / self.pastbal[-1]
        sharpe_roi = self.pastroi.copy()
        sharpe_roi.append(latest_roi)
        reward = np.mean(sharpe_roi) / np.std(sharpe_roi)  # sharpe ratio
        self.state[-1] = reward
        if (self.timestamp - self.startime) % 86400000 == 0:
            self.pastbal.append(self.state[0])
            self.pastroi.append(
                (self.pastbal[-1] - self.pastbal[-2]) / self.pastbal[-2]
            )
        # Check if shower is done
        if self.timestamp == self.endtime or self.state[0] <= 0:
            done = True
        else:
            done = False

        # Apply temperature noise
        # self.state += random.randint(-1,1)
        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info

    def render(self):
        print(f"Current balance: {self.state[0]}, Sharpe Ratio: {self.state[-1]}")
        return

    def reset(self, df=None):
        self.state = np.array([10000, 10000, 0, 0, 0, 0, 0])
        self.pastbal = [10000]
        self.pastroi = []
        if not df is None:
            self.df = df
        self.timestamp = df["timestamp"].values[0]
        return self.state


"""
Balance 100, leverage 2x
Buy 100% -- 200 usdt value
sell 100%


"""
