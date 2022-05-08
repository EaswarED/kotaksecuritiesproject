import os
import pandas
import pandas as pd
import requests
import json
import numpy
import time
import re, uuid
import xlwings as xw
from modules.WebSocket.WebSocketAPI import WebSocketAPI
from netifaces import interfaces, ifaddresses, AF_INET
from openpyxl import load_workbook, Workbook
from string import ascii_uppercase
from openpyxl.utils import get_column_letter

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
apikey = '0NF3bM0s'
username = 'R694288'
pwd = 'Amieshu2203@'
df_data = ''

directory = os.getcwd()

def authenication_smart_api():
    endpoint_url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': localIP,
        'X-ClientPublicIP': publicIP,
        'X-MACAddress': macAddress,
        'X-PrivateKey': apikey
    }

    payload = {
        "clientcode": username,
        "password": pwd
    }
    response = requests.post(url=endpoint_url, headers=headers, data=json.dumps(payload)).json()
    print("Authenication", response)
    return response


def generate_token():
    endpoint_url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/jwt/v1/generateTokens"
    refresh_token_data = authenication_smart_api()
    refresh_token = refresh_token_data['data']['refreshToken']
    jwtToken = refresh_token_data['data']['jwtToken']
    payload = {
        "refreshToken": refresh_token
    }
    headers = {
        'Authorization': 'Bearer {}'.format(jwtToken),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': localIP,
        'X-ClientPublicIP': publicIP,
        'X-MACAddress': macAddress,
        'X-PrivateKey': apikey
    }

    response = requests.post(url=endpoint_url, headers=headers, data=json.dumps(payload)).json()
    print("Generating TOken", response)
    return response


def user_profile():
    token_data = generate_token()
    endpoint_url = "	https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getProfile"
    headers = {
        'Authorization': 'Bearer {}'.format(token_data['data']['jwtToken']),
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': '192.168.169.37',
        'X-ClientPublicIP': '192.168.169.37',
        'X-MACAddress': '30:8d:99:bd:44:8c',
        'X-PrivateKey': apikey
    }

    response = requests.get(url=endpoint_url, headers=headers).json()
    print("Finally getting user profile", response)
    print(response)


def get_instrument():
    endpoint_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url=endpoint_url).json()
    return response


def getTokenInfo(instrumentName, exchange, instrumentType="", Segment="", strike=0, expiry=''):
    df_data = pandas.DataFrame(get_instrument())
    print(df_data)
    eq_df = df_data[(df_data.exch_seg == exchange) & (df_data.name == instrumentName)]

    return eq_df.iloc[0]


Live_Data = {}
def get_live_data():
    instrument_data = get_instrument() #getting list stock
    df_instrument = pd.DataFrame(instrument_data) # set data frame like table

    FEED_TOKEN_DATA = generate_token() # generating token and feed token
    FEED_TOKEN = FEED_TOKEN_DATA['data']['feedToken']
    instruments = [{'name': 'SBIN', 'exchange': 'NSE'},
                   {'name': 'NIFTY', 'exchange': 'NSE'},
                   {'name': 'RELIANCE', 'exchange': 'NSE'},
                   {'name': 'GAL', 'exchange': 'NSE'}]
    token_data = ''
    token = 'nse_cm|2885&nse_cm|25&nse_cm|15083&nse_cm|3499&nse_cm|16675&nse_cm|2475&nse_cm|14977&nse_cm|1394&nse_cm|4717'  # SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
    # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
    task = "mw"  # mw|sfi|dp
    #set interval user name token
    ss = WebSocketAPI(FEED_TOKEN, username, 5000)
    s1 = set(['tk', 'ltp', 'bp', 'sp', 'cng', 'lo', 'v', 'ap'])
    Live_Data["data"] = []
    #getting response like live data
    def on_message(ws, message):
        tickers = message
        print(message)
        stock_list={}
        #looping each data of interating from array
        for stock in message:
            # Live_Data['data'].append({
            #     'token':stock['name'],
            #     "date":stock['tvalue']
            # })
            if not 'tvalue' in stock and not 'ak' in stock and s1.issubset(stock.keys()):

                stock_list= {
                                    "Token": stock["tk"],
                                    "Ltp": stock["ltp"],
                                    "Close":stock['c'],
                                    "Best Buy price": stock["bp"],
                                    "Best sell price": stock["sp"],
                                    "Change": stock["cng"],
                                    "Low": stock["lo"],
                                    # "High": stock["h"],
                                    # "Open": stock["op"],
                                    "Volume": stock["v"],
                                    "VWAP": stock["ap"]
                }
        if stock_list:
            Live_Data['data'].append(stock_list)
            print(Live_Data)

        if Live_Data['data']:
            #set live data of list above that
            df = pandas.DataFrame(Live_Data['data'])

            #when merging instruments and live data which compared on based selected token and tk
            df1 = pd.merge(df_instrument, df, left_on=['token'], right_on=['Token'], how="inner")
            #getting current dictionary folder
            #getting today time
            ts = time.time()


            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')

            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name='Sheet1', index=False)

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


if __name__ == "__main__":
    get_live_data()
