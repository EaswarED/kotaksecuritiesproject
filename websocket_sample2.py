import asyncio
import base64
import json
import ssl
import zlib

import pandas as pd
import numpy as np
import websockets

import index
from modules.WebSocket.WebSocketAPI import WebSocketAPI

FEED_TOKEN_DATA = index.generate_token()  # generating token and feed token
FEED_TOKEN = FEED_TOKEN_DATA['data']['feedToken']

task = "mw"  # mw|sfi|dp
ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
s1 = set(['tk', 'ltp', 'bp', 'sp', 'cng', 'lo', 'v', 'ap'])
live_data =dict()
live_data["data"] = []

instrument_data = index.get_instrument()  # getting list stock
df_instrument = pd.DataFrame(instrument_data)  # set data frame like table

def live_data_rsi(interval):

    FEED_TOKEN_DATA = index.generate_token()  # generating token and feed token
    FEED_TOKEN = FEED_TOKEN_DATA['data']['feedToken']

    #put 10 list of stocks
    token = 'nse_cm|2885&nse_cm|25&nse_cm|15083&nse_cm|3499&nse_cm|16675&nse_cm|2475&nse_cm|14977&nse_cm|1394&nse_cm|4717'  # SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
    # set interval user name token
    ss = WebSocketAPI(FEED_TOKEN, index.username, interval)
    s1 = set(['tk', 'ltp', 'bp', 'sp', 'cng', 'lo', 'v', 'ap'])
    live_data["data"] = []

    # getting response like live data
    def on_message(ws, message):

        print(message)#getting response from websocket modules
        stock_list = {}#set default of dictionary
        for stock in message:# looping each data of interating from array
            if s1.issubset(stock.keys()): #check if all element is existing key
                stock_list = {
                    "Token": stock["tk"],
                    "Ltp": stock["ltp"],
                    "Close": stock['c'],
                    "Best_Buy_price": stock["bp"],
                    "Best_sell_price": stock["sp"],
                    "Change": stock["cng"],
                    "Low": stock["lo"],
                    "Volume": stock["v"],
                    "VWAP": stock["ap"]
                }

        if stock_list:#check if stock_list is existing r not
            live_data['data'].append(stock_list) #adding data to array

        if live_data['data']:#check if data is existing r not
            df = pd.DataFrame(live_data['data'])# set live data of list above that

            df['Close'] = df['Close'].astype(float).astype(np.int64) #converting string to number
            df['change'] = round(df['Close'].diff(), 2)
            df['gain'] = round(df.change.mask(df.change < 0, 0.0), 2)
            df['loss'] = round(-df.change.mask(df.change > 0, -0.0), 2)
            df['avg_gain'] = np.nan#below 14 row, means set None or 0
            df['avg_loss'] = np.nan#below 14 row, means set None or 0

            n = 14  # set default for RSI

            df['avg_gain'][n] = df['gain'].rolling(window=n).mean().dropna().iloc[0]
            df['avg_loss'][n] = df['loss'].rolling(window=n).mean().dropna().iloc[0]
            # above row 14, put +ve to gain or -ve to loss
            df['avg_gain'][n] = df.loc[:n, 'gain'].mean()
            df['avg_loss'][n] = df.loc[:n, 'loss'].mean()

            for i in range(n + 1, df.shape[0]):
                #(previous gain * (14-1) + current gain) / 14 => formula
                df['avg_gain'].loc[i] = (df['avg_gain'].loc[i - 1] * (n - 1) + df['gain'].loc[i]) / n
                df['avg_loss'].loc[i] = (df['avg_loss'].loc[i - 1] * (n - 1) + df['loss'].loc[i]) / n

            #average gain / average loss and round means 0.0 instead of 0.00000
            df['rs'] = round(df.avg_gain / df.avg_loss, 2)
            # 100-(100 / (1*rs)) and round means 0.0 instead of 0.00000
            df['rsi_14'] = round(100 - (100 / (1 + df.rs)), 2)

            # (0.6* rsi_14) + 20 and round means 0.0 instead of 0.00000
            df['altered_rsi_value'] = round((0.6 * df.rsi_14) + 20, 2)
            # rsi_14 - altered RSI value and round means 0.0 instead of 0.00000
            df['diff'] = round(df.rsi_14 - df.altered_rsi_value, 2)

            df1 = pd.merge(df_instrument, df, left_on=['token'], right_on=['Token'], how="inner")# when merging instruments and live data which compared on based selected token and tk
            #Filtered columns with needed of header
            df1= df1[df1.columns.intersection({'Close':'close','change':'change', 'gain':'gain', 'loss':'loss', 'avg_gain':'average_gain', 'avg_loss':'average_loss', 'rs':'rsi', 'rsi_14':'rsi_14', 'token':'token', 'symbol':'symbol', 'name':'name'})]
            #returning df1 value
            return df1

    def on_open(ws):
        print("on open")
        ss.subscribe(task, token)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("Close")

    # Assign the callbacks.
    ss._on_open = on_open
    ss._on_message = on_message
    ss._on_error = on_error
    ss._on_close = on_close

    ss.connect()




if __name__ == '__main__':
    #set list like array
    #tokens_data = ["2885", "25", "15083", "3499", "16675", "2475", "14977", "1394", "4717"]

    df_5min = live_data_rsi(5)#Market live data with 5min interval
    # df_15min = live_data_rsi(15)
    # df_30min = live_data_rsi(30)
    # df_1hour = live_data_rsi(60)

    writer = pd.ExcelWriter('{}.xlsx'.format("rsi_data"), engine='xlsxwriter') #creating new excel file
    df_5min.to_excel(writer, sheet_name='5min', index=False)#rename sheet name from created file
    # df_30min.to_excel(writer, sheet_name='30min', index=False)
    # df_1hour.to_excel(writer, sheet_name='1hour', index=False)
    # df_15min.to_excel(writer, sheet_name='15min', index=False)
    writer.save()#retrieving data and saving data to created file
