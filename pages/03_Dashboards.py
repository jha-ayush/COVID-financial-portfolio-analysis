from PIL import Image
import pandas as pd
import numpy as np
from pathlib import Path
import fire 
# import questionary
import os
import json
import requests
import sqlalchemy
from dotenv import load_dotenv
from MCForecastTools import MCSimulation
import datetime
from time import sleep
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
from pytz import timezone
import pyfolio as pf
import matplotlib
import re
import streamlit as st

# Set page configurations - ALWAYS at the top
st.set_page_config(page_title="COVID portfolio analyzer",page_icon=":bar_chart:",layout="wide")


# Use local style.css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
        
local_css("style/style.css")
        

# Visualizations
with st.container():
    st.header("Dashboards")
    st.write("---")

def get_prices(start_date,end_date,universe):
    data = pd.DataFrame()
    # end_at = datetime.datetime.now() 
    # begin_from = end_at + datetime.timedelta(days=-5000)
    for t in tqdm(universe):
        print(t)
        print(len(data))
        # for start in pd.date_range(start = begin_from, end = end_at,normalize=True,freq = '88D'):
        #     end = start + datetime.timedelta(days = 88)
        #     end = str(int((end - datetime.datetime(1970,1,1)).total_seconds()))
        #     start = str(int((start - datetime.datetime(1970,1,1)).total_seconds()))
        try:
            r = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{t}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}')
        except json.JSONDecodeError:
            pass
        try:
            # print(r.json())
            temp_data = pd.DataFrame(r.json()['results'])
            temp_data['ticker'] = t
            data = data.append(temp_data, ignore_index=True)
            print(t+':'+str(pd.to_datetime(start_date, unit='s'))+':'+str(pd.to_datetime(end_date, unit='s')))
        except KeyError:
            print(f'{t} was not found')
            pass
        except ValueError:
            pass
        except ConnectionError as error:
            print(error)
            sleep(200)
            continue
        except TimeoutError as error:
            print(error)
            sleep(200)
            continue
        sleep(0.25)
#     data.to_csv(file_name,index = False)
    data.t = pd.to_datetime(data.t, unit = 'ms')
    columns_name = {'t': 'time', 'o': 'Open', 'c': 'Close', 'h': 'High', 'l': 'Low', 'v': 'Volume'} 
    data= data.rename(columns = columns_name)
    data = data[['time','ticker','Open', 'Close','High', 'Low', 'Volume']]
    data = data.set_index(['time', 'ticker'])
    data["daily_returns"] = data['Close'].groupby('ticker').pct_change()
    data = data.dropna()
    #data.to_csv(file_name, index = False)
    return data

# Display visualizations - dashboards
user_choice_period = st.selectbox(
    'What period?',
    ('pre', 'pan', 'post'))                                

if user_choice_period == "pre-pandemic":
    start_date = "2017-03-01"
    end_date = "2020-02-29"
elif user_choice_period == "pandemic":       
    start_date = "2020-03-01"
    end_date = "2021-02-29"
elif user_choice_period == "post-pandemic":
    start_date = "2021-03-01"
    end_date = "2022-03-01"