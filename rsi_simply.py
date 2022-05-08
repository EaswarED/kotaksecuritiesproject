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

tokens = ["2885"] #, "25", "15083", "3499", "16675","2475", "14977", "1394","4717"

def get_historial_data():
    j=0
    resp_instrument = index.get_instrument()
    df_instrument = pd.DataFrame(resp_instrument)
    while j< len(tokens):

        payload= dict(exchange="NSE", symboltoken=tokens[j], interval="FIFTEEN_MINUTE", fromdate="2022-03-01 09:00",
                      todate="2022-03-02 15:16")
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
        df['change'] = df['close'].diff()
        df['gain'] = df.change.mask(df.change < 0, 0.0)
        df['loss'] = -df.change.mask(df.change > 0, -0.0)
        df['avg_gain'] = rma(df.gain[n + 1:].to_numpy(), n, np.nansum(df.gain.to_numpy()[:n + 1]) / n)
        df['avg_loss'] = rma(df.loss[n + 1:].to_numpy(), n, np.nansum(df.loss.to_numpy()[:n + 1]) / n)
        df['rs'] = df.avg_gain / df.avg_loss
        df['rsi_14'] = 100 - (100 / (1 + df.rs))
        print(df)
        df1 = pd.merge(df, df_instrument, left_on=['tk'],right_on=['token'],how="inner")
        df1.columns = ['Timestamp','change', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rs', 'rsi_14', 'token', 'symbol', 'name']
        print(df1)
        df.to_csv("/home/edmonster/Downloads/{}.csv".format(tokens[j]))

        j+=1

def rma(x, n, y0):
    a = (n-1) / n
    ak = a**np.arange(len(x)-1, -1, -1)
    return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1)]

def get_order_data():
    j=0
    while j< len(tokens):
        payload= dict(exchange="NSE", symboltoken=tokens[j], tradingsymbol= "RELIANCE-EQ")
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
        response = requests.post(url="https://apiconnect.angelbroking.com/order-service/rest/secure/angelbroking/order/v1/getLtpData", data=json.dumps(payload), headers=headers).json()
        print(response)
        df = pd.DataFrame(response['data'])
        print(df)
        return df


if __name__ == '__main__':
    get_historial_data()


