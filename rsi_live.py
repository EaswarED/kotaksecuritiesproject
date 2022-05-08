import time

import index
import pandas as pd
from modules.WebSocket.WebSocketAPI import WebSocketAPI
import numpy as np

live_data={}

instrument_data = index.get_instrument()  # getting list stock
df_instrument = pd.DataFrame(instrument_data)  # set data frame like table

def live_data_rsi():

    FEED_TOKEN_DATA = index.generate_token()  # generating token and feed token
    FEED_TOKEN = FEED_TOKEN_DATA['data']['feedToken']

    token = 'nse_cm|2885&nse_cm|25&nse_cm|15083&nse_cm|3499&nse_cm|16675&nse_cm|2475&nse_cm|14977&nse_cm|1394&nse_cm|4717'  # SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
    task = "mw"  # mw|sfi|dp
    # set interval user name token
    ss = WebSocketAPI(FEED_TOKEN, index.username, 3)
    s1 = set(['tk', 'ltp', 'bp', 'sp', 'cng', 'lo', 'v', 'ap'])
    live_data["data"] = []

    # getting response like live data
    def on_message(ws, message):
        stock_list = {}
        # looping each data of interating from array
        for stock in message:
            if not 'tvalue' in stock and not 'ak' in stock and s1.issubset(stock.keys()):
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
        if stock_list:
            live_data['data'].append(stock_list)

        if live_data['data']:
            # set live data of list above that
            df = pd.DataFrame(live_data['data'])
            # when merging instruments and live data which compared on based selected token and tk
            df['Close'] = df['Close'].astype(float).astype(np.int64)
            df['change'] = round(df['Close'].diff(), 2)
            df['gain'] = round(df.change.mask(df.change < 0, 0.0), 2)
            df['loss'] = round(-df.change.mask(df.change > 0, -0.0), 2)
            df['avg_gain'] = np.nan
            df['avg_loss'] = np.nan

            n = 14  # what is the window

            df['avg_gain'][n] = df['gain'].rolling(window=n).mean().dropna().iloc[0]
            df['avg_loss'][n] = df['loss'].rolling(window=n).mean().dropna().iloc[0]
            # Alternatively
            df['avg_gain'][n] = df.loc[:n, 'gain'].mean()
            df['avg_loss'][n] = df.loc[:n, 'loss'].mean()

            for i in range(n + 1, df.shape[0]):
                df['avg_gain'].loc[i] = (df['avg_gain'].loc[i - 1] * (n - 1) + df['gain'].loc[i]) / n
                df['avg_loss'].loc[i] = (df['avg_loss'].loc[i - 1] * (n - 1) + df['loss'].loc[i]) / n

            df['rs'] = round(df.avg_gain / df.avg_loss, 2)
            df['rsi_14'] = round(100 - (100 / (1 + df.rs)), 2)

            df['altered_rsi_value'] = round((0.6 * df.rsi_14) + 20, 2)

            df['diff'] = round(df.rsi_14 - df.altered_rsi_value, 2)

            df1 = pd.merge(df_instrument, df, left_on=['token'], right_on=['Token'], how="inner")
            print("Dictionary",df1.to_dict(orient='records'))
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')

            # Convert the dataframe to an XlsxWriter Excel object.
            df1.to_excel(writer, sheet_name='Sheet1', index=False)

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()

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
    live_data_rsi()