import asyncio
import base64
import json
import ssl
import zlib

import pandas as pd
import numpy as np
import websockets

import index

FEED_TOKEN_DATA = index.generate_token()  # generating token and feed token
FEED_TOKEN = FEED_TOKEN_DATA['data']['feedToken']

token = 'nse_cm|2885'  # SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
task = "mw"  # mw|sfi|dp
ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
s1 = set(['tk', 'ltp', 'bp', 'sp', 'cng', 'lo', 'v', 'ap'])
live_data =dict()
live_data["data"] = []

async def hello(interval, tokens):
    async with websockets.connect("wss://wsfeeds.angelbroking.com/NestHtml5Mobile/socket/stream",ssl=ssl_context) as webs:
        while 1:
            try:
                request = {"task": task, "channel": tokens+"&nse_cm", "token": FEED_TOKEN, "user": index.username,
                   "acctid": index.username}
                await webs.send(json.dumps(request))
                await asyncio.sleep(interval)

                greeting = await webs.recv()
                data = base64.b64decode(greeting)

                try:
                    data = bytes((zlib.decompress(data)).decode("utf-8"), 'utf-8')
                    data = json.loads(data.decode('utf8').replace("'", '"'))
                    data = json.loads(json.dumps(data, indent=4, sort_keys=True))

                except ValueError:
                    return

                if data:
                    print(f"< {data}")
                    stock_list = {}
                    for stock in data:
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
                        print("df_result",df)
                        return df

            except Exception as e:
                print(e)


if __name__ == '__main__':
    tokens_data = ["2885", "25", "15083", "3499", "16675", "2475", "14977", "1394", "4717"]
    j=0
    while j <len(tokens_data):
        asyncio.get_event_loop().run_until_complete(hello(5,tokens_data[j]))
        asyncio.get_event_loop().run_until_complete(hello(15,tokens_data[j]))
        asyncio.get_event_loop().run_until_complete(hello(30,tokens_data[j]))
        asyncio.get_event_loop().run_until_complete(hello(60,tokens_data[j])) #1 hour
        asyncio.get_event_loop().run_forever()
        df_5min = hello(5,tokens_data[j])
        df_15min = hello(15,tokens_data[j])
        df_30min = hello(30,tokens_data[j])
        df_1hour = hello(60,tokens_data[j])
        writer = pd.ExcelWriter('{}.xlsx'.format(tokens_data[j]), engine='xlsxwriter')
        df_5min.to_excel(writer, sheet_name='5min', index=False)
        df_30min.to_excel(writer, sheet_name='30min', index=False)
        df_1hour.to_excel(writer, sheet_name='1hour', index=False)
        df_15min.to_excel(writer, sheet_name='15min', index=False)
        writer.save()