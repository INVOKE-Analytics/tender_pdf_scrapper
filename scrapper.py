import pandas as pd
import requests
import numpy as np
import time 
from bs4 import BeautifulSoup
from datetime import date

import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

pd.set_option('max_colwidth', 400)

disable_warnings(InsecureRequestWarning)

_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

# RFQ INVITATION
link = "https://msmart.mcmc.gov.my"
html_text = requests.get(link, headers=_headers, verify=False).text
soup = BeautifulSoup(html_text, 'lxml')

def get_df(tab_name:str):
    # tab_name = "rfq"
    table = soup.find("div", {"id":tab_name})

    # get colname
    colname = []
    for i in table.find_all('th'):
        title = i.text
        colname.append(title)

    df_ = pd.DataFrame(columns=colname)

    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        lenght = len(df_)
        df_.loc[lenght] = row

    all_id = []
    for p in table.find_all('tr')[1:]:
        link = p.find_all("a", href=True)
        roi = link[0]
        try:
            tender = link[1]
            tender = tender['href']
            tender = str(tender)
            id_ = tender[tender.find('id')+3:]
            all_id.append(f"https://msmart.mcmc.gov.my/web/index.php?r=site/print-rfp-tender-info&id={id_}")
        except:
            all_id.append(np.NAN)

    # SEPERATE DATE AND TIME 
    open_date_list = df_["Issuance Date"].to_list()
    close_date_list = df_["Closing Date"].to_list()

    da = [_open[:_open.find('2022')+4] if '2022' in _open else _open[:_open.find('2021')+4] for _open in open_date_list]
    dc = [_close[:_close.find('2022')+4] if '2022' in _close else _close[:_close.find('2021')+4] for _close in close_date_list]
    to = [_open[_open.find('2022')+4:] if '2022' in _open else _open[:_open.find('2021')+4] for _open in open_date_list]
    tc = [_close[_close.find('2022')+4:] if '2022' in _close else _close[:_close.find('2021')+4] for _close in close_date_list]

    df_copy = df_.copy()
    df_copy["Date Open"] = pd.Series(da)
    df_copy["Time Open"] = pd.Series(to)
    df_copy["Date Close"] = pd.Series(dc)
    df_copy["Time Close"] = pd.Series(tc)

    df_copy['PDF Link'] = pd.Series(all_id)

    # FILTERING DATA SCIENCE/IT SERVICE CONTEXT ONLY
    df_new = df_copy.copy()

    # filter layer: phrase exist 
    #df_new = df_new[df_new['Related Work Categories'].str.contains('IT SERVICES')]

    #df_new = df_new[df_new['Date Open'].dt.month == 11]


    df_new = df_new[['Date Open', 'Time Open', 'Date Close',
        'Time Close', 'Title' ,'PDF Link']]

    return df_new

# COMPLETED