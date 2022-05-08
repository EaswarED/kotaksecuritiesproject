import pandas as pd
import requests
import pandas
from netifaces import interfaces, ifaddresses, AF_INET
import re, uuid
import index
import json
import numpy as np

api_url="https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"
apikey = '0NF3bM0s'
username = 'R694288'
pwd = 'Amieshu2203@'
n = 14

addresses = []
publicIP = ''
localIP = ''

for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': ' '}])]
    if not ' ' in addresses:
        ip_address = ' '.join(addresses)
        if ip_address != '127.0.0.1':
            publicIP = ip_address
        else:
            localIP = ip_address

macAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
print(localIP, publicIP, macAddress)

tokens = ["2885","25", "15083", "3499", "16675","2475", "14977", "1394","4717"] #,

def get_historial_data():
    j=0
    resp_instrument = index.get_instrument()
    df_instrument = pd.DataFrame(resp_instrument)
    while j< len(tokens):

        payload= dict(exchange="NSE", symboltoken=tokens[j], interval="FIFTEEN_MINUTE", fromdate="2022-02-27 09:00",
                      todate="2022-02-28 15:16")
        headers={
            'X-PrivateKey': apikey,
            'Accept': 'application/json',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': localIP,
            'X-ClientPublicIP': publicIP,
            'X-MACAddress': macAddress,
            'X-UserType': 'USER',
            'Authorization': 'Bearer {}'.format(index.authenication_smart_api()['data']['jwtToken']),
            'Content-Type': 'application/json'
        }
        print(headers,payload)
        response = requests.post(url=api_url, data=json.dumps(payload), headers=headers).json()
        print(response)
        columns = ['Timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(response['data'],columns=columns)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Timestamp']= df['Timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %I:%M %p'))
        df['tk'] = tokens[j]
        df['change'] = round(df['close'].diff(),2)
        df['gain'] = round(df.change.mask(df.change < 0, 0.0),2)
        df['loss'] = round(-df.change.mask(df.change > 0, -0.0),2)
        df['avg_gain'] = np.nan
        df['avg_loss'] = np.nan
        n = 14  # what is the window
        # keep first occurrence of rolling mean
        df['avg_gain'][n] = df['gain'].rolling(window=n).mean().dropna().iloc[0]
        df['avg_loss'][n] = df['loss'].rolling(window=n).mean().dropna().iloc[0]
        # Alternatively
        df['avg_gain'][n] = df.loc[:n, 'gain'].mean()
        df['avg_loss'][n] = df.loc[:n, 'loss'].mean()
        # This is not a pandas way, looping through the pandas series, but it does what you need
        for i in range(n + 1, df.shape[0]):
            df['avg_gain'].iloc[i] = (df['avg_gain'].iloc[i - 1] * (n - 1) + df['gain'].iloc[i]) / n
            df['avg_loss'].iloc[i] = (df['avg_loss'].iloc[i - 1] * (n - 1) + df['loss'].iloc[i]) / n

        df['rs'] = round(df.avg_gain / df.avg_loss,2)
        df['rsi_14'] = round(100 - (100 / (1 + df.rs)),2)

        df['altered_rsi_value'] = round((0.6*df.rsi_14)+20,2)

        df['diff'] = round(df.rsi_14 - df.altered_rsi_value,2)
        df.sort_values(["diff"], ascending=False)
        sorted_df = df.sort_values(["diff"], ascending=True)

        print(df)
        writer = pd.ExcelWriter('{}.xlsx'.format(tokens[j]), engine='xlsxwriter')

        df.to_excel(writer, sheet_name='one HOurs', index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        j+=1


def df_loop_data(df):
    c = 0
    prices = []
    print("DF",df)
    while c < len(df):
        print(df.iloc[c, 14])
        if df.iloc[c, 14] > float(2.00):  # Check that the closing price for this day is greater than $2.00
            prices.append(df.iloc[c, 14]) #called change like LTP
        c += 1
    return prices

if __name__ == '__main__':
    get_historial_data()


