import pandas as pd
import requests
import pandas
from netifaces import interfaces, ifaddresses, AF_INET
import re, uuid
import index
import json
import numpy as np

api_url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"
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

tokens = ["16675","2885","25"]


def get_historial_data():
    top_ranking_3min = []
    top_ranking_15min = []
    top_ranking_30min = []
    top_ranking_1hour = []
    top_ranking_oneday = []
    top_ranking_3min1 = []
    top_ranking_15min1 = []
    top_ranking_30min1 = []
    top_ranking_1hour1 = []
    j = 0
    while j < len(tokens):
        resp_instrument = index.get_instrument()
        df_instrument = pd.DataFrame(resp_instrument)
        df_instrument = df_instrument[(df_instrument['token'] == tokens[j]) & (df_instrument['exch_seg'] == 'NSE')]
        columns = {'token':'tokenId', 'symbol':'symbol','name':'tokenName'}
        df_instrument = df_instrument[df_instrument.columns.intersection(columns)]

        df_3min = df_interval_data(tokens[j], "THREE_MINUTE", "NSE", "2022-01-01 09:15", "2022-03-21 15:16", desc=True)
        df_15min = df_interval_data(tokens[j], "FIFTEEN_MINUTE", "NSE", "2022-01-01 09:15", "2022-03-21 15:16",
                                    desc=True)
        df_30min = df_interval_data(tokens[j], "THIRTY_MINUTE", "NSE", "2022-01-01 09:15", "2022-03-21 15:16",
                                    desc=True)
        df_1hour = df_interval_data(tokens[j], "ONE_HOUR", "NSE", "2022-01-01 09:15", "2022-03-21 15:16", desc=True)
        # df_1day = df_interval_data(tokens[j], "ONE_DAY", "NSE", "2022-03-01 09:15", "2022-03-21 15:16", desc=True)

        writer = pd.ExcelWriter('{}.xlsx'.format(df_instrument['name'].values[0]), engine='xlsxwriter')

        df_3min.to_excel(writer, sheet_name='3min', index=False)
        df_15min.to_excel(writer, sheet_name='15min', index=False)
        df_30min.to_excel(writer, sheet_name='30min', index=False)
        df_1hour.to_excel(writer, sheet_name='1Hour', index=False)
        # df_1day.to_excel(writer, sheet_name='OneDay', index=False)
        # xls = pd.ExcelFile(
        #     '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]))
        writer.save()
        df3min = pd.read_excel(
            '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]),
            sheet_name="3min")
        df15min = pd.read_excel(
            '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]),
            sheet_name="15min")
        df30min = pd.read_excel(
            '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]),
            sheet_name="30min")
        df1hour = pd.read_excel(
            '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]),
            sheet_name="1Hour")
        # dfoneday = pd.read_excel(
        #     '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]),
        #     sheet_name="OneDay")
        print(df3min['total'].max())
        top_ranking_3min.append({
            "name":df_instrument['name'].values[0],
            "ranking_value":df3min['total'].max()
        })
        top_ranking_15min.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df15min['total'].max()
        })
        top_ranking_30min.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df30min['total'].max()
        })
        top_ranking_1hour.append({
            "name":df_instrument['name'].values[0],
            "ranking_value":df1hour['total'].max()
        })

        print(df3min['total'].max())
        top_ranking_3min1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df3min['total'].min()
        })
        top_ranking_15min1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df15min['total'].min()
        })
        top_ranking_30min1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df30min['total'].min()
        })
        top_ranking_1hour1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df1hour['total'].min()
        })

        # top_ranking_oneday.append({
        #     "name":df_instrument['name'].values[0],
        #     "ranking_value":dfoneday['total'].max()
        # })
        print("----------------3 min --------------------")
        df1 = pd.DataFrame(top_ranking_3min)
        df1 = df1.sort_values(by=['ranking_value'], ascending=False)
        df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test1.csv')
        print(df1)
        print("----------------15 min --------------------")
        df2 = pd.DataFrame(top_ranking_15min)
        df2 = df2.sort_values(by=['ranking_value'], ascending=False)
        df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test2.csv')
        print(df2)
        print("----------------30 min --------------------")
        df3 = pd.DataFrame(top_ranking_30min)
        df3 = df3.sort_values(by=['ranking_value'], ascending=False)
        df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test3.csv')
        print(df3)
        print("----------------1 hour --------------------")
        df4 = pd.DataFrame(top_ranking_1hour)
        df4 = df4.sort_values(by=['ranking_value'], ascending=False)

        print(df4)
        # print("----------------One day --------------------")
        # df5 = pd.DataFrame(top_ranking_oneday)
        # df5 = df5.sort_values(by=['ranking_value'], ascending=False)
        # print(df5)
        print("----------------3 min --------------------")
        df5 = pd.DataFrame(top_ranking_3min1)
        df5 = df5.sort_values(by=['ranking_value'], ascending=False)

        print(df5)
        print("----------------15 min --------------------")
        df6 = pd.DataFrame(top_ranking_15min1)
        df6 = df6.sort_values(by=['ranking_value'], ascending=False)

        print(df6)
        print("----------------30 min --------------------")
        df7 = pd.DataFrame(top_ranking_30min1)
        df7 = df7.sort_values(by=['ranking_value'], ascending=False)

        print(df7)
        print("----------------1 hour --------------------")
        df8 = pd.DataFrame(top_ranking_1hour1)
        df8 = df8.sort_values(by=['ranking_value'], ascending=False)

        print(df8)

        j += 1
        return df1,df2,df3,df4,df5,df6,df7,df8

def df_interval_data(token, intervals, exchanges, from_date, to_date, desc=False):
        payload = dict(exchange=exchanges, symboltoken=token, interval=intervals, fromdate=from_date,
                       todate=to_date)
        headers = {
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

        response = requests.post(url=api_url, data=json.dumps(payload), headers=headers).json()

        columns = ['Timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(response['data'], columns=columns)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Timestamp'] = df['Timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %I:%M %p'))

        columns = ['Timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(response['data'], columns=columns)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Timestamp'] = df['Timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %I:%M %p'))
        df['tk'] = token
        df['change'] = round(df['close'].diff(), 2)
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
        #checking if values has negative or not means append positive or negative in column sign
        df['sign'] = np.where(df['diff'].isnull(), np.nan,
                           np.where(df['diff'] > 0, 'Positive', 'Negative'))
        df['ranking_value'] = 0
        df['ranking']=np.nan
        index_column = []
        res_values = []
        res_date=[]

        print(df)
        for i in range(n + 1, df.shape[0]):
            if (df.iloc[i]['sign'] == 'Positive' and df.iloc[i-1]['sign'] == 'Negative'): #check previous value and current value
                index_column.append(i)
                index_column.append(i+1)
                df['ranking_value'].iloc[i] = df.iloc[i-1]['rsi_14'] #previous value
                df['ranking_value'].iloc[i+1] = df.iloc[i]['rsi_14'] #current value
                res_values.append(df['ranking_value'].iloc[i])
                res_values.append(df['ranking_value'].iloc[i+1])
                res_date.append(df['Timestamp'].iloc[i])
                res_date.append(df['Timestamp'].iloc[i + 1])

            elif (df.iloc[i]['sign'] == 'Negative' and df.iloc[i-1]['sign'] == 'Positive'):
                index_column.append(i)
                index_column.append(i + 1)

                df['ranking_value'].iloc[i] = df.iloc[i - 1]['rsi_14']  # previous value
                df['ranking_value'].iloc[i + 1] = df.iloc[i]['rsi_14']  # current value
                res_values.append(df['ranking_value'].iloc[i])
                res_values.append(df['ranking_value'].iloc[i + 1])
                res_date.append(df['Timestamp'].iloc[i])
                res_date.append(df['Timestamp'].iloc[i + 1])

        df_d = pd.DataFrame({
            'indec_no': index_column,
            'values': res_values,
            'date':res_date
        })
        print(df_d)
        nss=0
        df_d['total']=0
        for i in range(nss + 1, df_d.shape[0]):
            print(df_d['values'][i-1], df_d['values'][i], i)
            df_d['total'].iloc[i] = df_d['values'][i-1] - df_d['values'][i]
        df_d = df_d[df_d['total'] != 0]
        print(df_d)
        df_d.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test.csv')
        df_final = pd.merge(df, df_d, left_on=['Timestamp'], right_on=['date'], how='left')

        columns = {'Timestamp': 'timestamp', 'open': 'open', 'high': 'high','low':'low','close':'close','tk':'token_id','change':'change',
        'gain':'gain','loss':'loss','avg_gain':'avg_gain','avg_loss':'avg_loss','rs':'rs','rsi_14':'rsi_14', 'altered_rsi_value':'altered_rsi_value','diff':'diff','ranking_value':'ranking_value','total':'ranking'}
        df_final = df_final[df_final.columns.intersection(columns)]

        print(df_final)
        return df_final


if __name__ == '__main__':
    get_historial_data()
