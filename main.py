from ks_api_client import ks_api
import requests
import pandas as pd
import csv
import re
import urllib3


consumer_key = "Qy5elcqxC9aKHpz8Fq1slfqsF5Aa"
access_token = "Bearer 5de6cc12-a089-36bc-b617-26e215e80904"

def main():

    url = "https://tradeapi.kotaksecurities.com/apim/scripmaster/1.1/filename"
    header={
        "consumerKey":consumer_key,
        "Authorization":access_token
    }

    filename = requests.get(url=url,headers=header)
    print(filename.content)
    resp_data = filename.json()
    print(resp_data['Success'])
    cash_data_url = resp_data['Success']['cash']

    df=pd.read_csv(cash_data_url,sep='|')
    df = df[(df['instrumentName'] == 'RELIANCE') | (df['instrumentName'] == 'ADANIENT')]
    print(df.to_dict('records'))
    # reader = csv.reader(open(cash_data, 'r'))
    # data_dict = {}
    # for row in reader:
    #     print(row)


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
      return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


if __name__ == '__main__':
    main()
