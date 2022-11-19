import pandas as pd
import numpy as np
from pathlib import Path
import fire 
import streamlit as s
import os
import json
import requests
import sqlalchemy
from dotenv import load_dotenv
import datetime
from time import sleep
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
from pytz import timezone
import pyfolio as pf
import matplotlib
import re

def get_prices(start_date,end_date,universe):
    data = pd.DataFrame()
    # end_at = datetime.datetime.now() 
    # begin_from = end_at + datetime.timedelta(days=-5000)
    for t in tqdm(universe):
        st.write(t)
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
            st.write(t+':'+str(pd.to_datetime(start_date, unit='s'))+':'+str(pd.to_datetime(end_date, unit='s')))
        except KeyError:
            st.write(f'{t} was not found')
            pass
        except ValueError:
            pass
        except ConnectionError as error:
            st.write(error)
            sleep(200)
            continue
        except TimeoutError as error:
            st.write(error)
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
    st.write(data)
    

def get_ticker_data_df(all_data, ticker_symbol):
    idx = pd.IndexSlice
    daily_returns_df = all_data.loc[idx[:,ticker_symbol],['daily_returns']]
    return daily_returns_df

def create_df(ticker_df_list,ticker_list):
    concat_df = pd.concat(ticker_df_list,axis=1, keys=ticker_list)
    return concat_df    

def create_mean_df(concat_df,ticker_type_list):
    mean_df=pd.DataFrame(concat_df.mean())
    mean_df=mean_df.reset_index()
    del mean_df['level_1']
    mean_df.columns=['Ticker','Mean']
    mean_df['Ticker_type']=ticker_type_list
    return mean_df

def create_std_df(concat_df,ticker_type_list):
    std_df=pd.DataFrame(concat_df.std())
    std_df=std_df.reset_index()
    del std_df['level_1']
    std_df.columns=['Ticker','Mean']
    std_df['Ticker_type']=ticker_type_list
    return std_df

def create_var_df():

def create_covar_df():


def create_connection():
    database_connection_string = 'sqlite:///'
    engine = sqlalchemy.create_engine(database_connection_string)
    #print(engine.table_names())
    return engine

def create_sql_table(mean_df):
    engine = create_connection()
    mean_df.to_sql('portfolio_mean',engine)
    return engine
    
def top_stock(engine):
    sel_max_mean="""select Ticker from portfolio_mean where mean= (select max(Mean) from portfolio_mean where Ticker_type='Stock')"""
    max_mean=list(engine.execute(sel_max_mean))
    if len(max_mean)==1:
        return str(max_mean[0])
    else:
        print("Check code")


def bottom_stock(engine):
    sel_min_mean="""select Ticker from portfolio_mean where mean= (select min(mean) from portfolio_mean where Ticker_type='Stock')"""
    min_mean=list(engine.execute(sel_min_mean))
    if len(min_mean)==1:
        return str(min_mean[0])
    else:
        print("Check code")

def top_etf(engine):
    sel_port_max_mean="""select Ticker from portfolio_mean where mean= (select max(Mean) from portfolio_mean where Ticker_type='ETF')"""
    max_mean=list(engine.execute(sel_port_max_mean))
    if len(max_mean)==1:
        return str(max_mean[0])
    else:
        print("Check code")

def bottom_etf(engine):
    sel_port_min_mean="""select Ticker from portfolio_mean where mean=(select min(mean) from portfolio_mean where Ticker_type='ETF')"""
    min_mean=list(engine.execute(sel_port_min_mean))
    if len(min_mean)==1:
        return str(min_mean[0])
    else:
        print("Check code")

def sur_spy(engine):
    sel_port_sur_spy="""select Ticker from portfolio_mean where Mean>0.020825"""
    sur_spy=list(engine.execute(sel_port_sur_spy))
    return str(sur_spy)
('AMZN',)
def get_ticker_string(str):
    match = re.search(r'\(\'([A-Z]+)\',\)', str)
    if match:
        return match.group(1)
    else:
        print("RE pattern match failed. Found str : {str}")
            
    
if __name__ == "__main__":
    
    user_choice_period = questionary.select("select a period?",choices = ["pre-pandemic","pandemic","postpandemic"]).ask()
    start_date=""
    end_date=""
    #ticker_list = 
    if user_choice_period == "pre-pandemic":
        start_date = "2017-03-01"
        end_date = "2020-02-29"
    elif user_choice_period == "pandemic":       
        start_date = "2020-03-01"
        end_date = "2021-02-29"
    elif user_choice_period == "post-pandemic":
        start_date = "2021-03-01"
        end_date = "2022-03-01"
    else:
        print("period not valid")
    user_choice_question = questionary.select("What would you like answers to\
                                 Choose 1 for: Which stock performed well\
                                 Choose 2 for: Which etf performed well\
                                 Choose 3 for: Which ticker performed better than SPY\
                                 Choose 4 for: Which stock performed inversely\
                                 Choose 5 for: Which ETF performed inversely?"
    ,choices = ["1","2","3","4","5"]).ask()

    
    ticker_list = ["AMZN", "RTH", "AMT", "IYR", "XOM", "XLE", "SPY"]
    ticker_type_list=['Stock','ETF','Stock','ETF','Stock','ETF','Index']
    POLYGON_API_KEY = 'JQfBpF3NpcYjuBdMiXeUr6q54XafY_pQ'
    all_data_df = get_prices(start_date,end_date,ticker_list)

    
    ticker_df_list = []
    for tk in ticker_list:
        ticker_df_list.append(get_ticker_data_df(all_data_df,tk))
    if len(ticker_df_list) != len(ticker_list):
        print("ticker df list length not matching ticker list")
             
    my_df = create_df(ticker_df_list,ticker_list)
    mean_df = create_mean_df(my_df, ticker_type_list)
    final_df = return_portf(mean_df)
    tech_return = tech_port_return(mean_df)
    
    #display(mean_df)
    mysqlengine= create_sql_table(mean_df)
    if user_choice_question =="1":
        mytopstock = get_ticker_string(top_stock(mysqlengine))
        print(f'{mytopstock} is top performing stock')
    elif user_choice_question =="2":
        mytopetf = get_ticker_string(top_etf(mysqlengine))
        print(f'{mytopetf} is top performing ETF')
    elif user_choice_question =="3":
        surspy=get_ticker_string(sur_spy(mysqlengine))
        print(f'{surspy} performed better than SPY')
    elif user_choice_question =="4":
        mybottomstock = get_ticker_string(bottom_stock(mysqlengine))
        print(f'{mybottomstock} is worst performing Stock')
    elif user_choice_question =="5":
        mybottometf = get_ticker_string(bottom_etf(mysqlengine))
        print(f'{mybottometf} is worst performing ETF')
    else:
        print('User choice is not valid')
    
    
    
    
    
