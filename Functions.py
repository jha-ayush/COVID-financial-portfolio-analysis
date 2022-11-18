import pandas as pd
import numpy as np
from pathlib import Path
import fire 
import questionary
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
from IPython.display import display
import matplotlib

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

def date_ranges():
    start_date = "2017-03-01"
    end_date = "2020-03-01"
    all_data = get_prices(start_date=start_date, end_date=end_date, universe=ticker_list)    
    return all_data

def get_ticker_data_df(all_data, ticker_symbol):
    idx = pd.IndexSlice
    daily_returns_df = all_data.loc[idx[:,ticker_symbol],['daily_returns']]
    return daily_returns_df
"""
def amzn_data(all_data):
    AMZN_daily_returns_df = all_data.loc[idx[:,'AMZN'],['daily_returns']]
    return AMZN_daily_returns_df

def rth_data(all_data):
    RTH_daily_returns_df = all_data.loc[idx[:,'RTH'],['daily_returns']]
    return RTH_daily_returns_df

def amt_data(all_data):
    AMT_daily_returns_df = all_data.loc[idx[:,'AMT'],['daily_returns']]
    return AMT_daily_returns_df

def iyr_data(all_data):
    IYR_daily_returns_df = all_data.loc[idx[:,'IYR'],['daily_returns']]
    return IYR_daily_returns_df

def xom_data(all_data):            
    XOM_daily_returns_df = all_data.loc[idx[:,'XOM'],['daily_returns']]
    return XOM_daily_returns_df

def xle_data(all_data):    
    XLE_daily_returns_df = all_data.loc[idx[:,'XLE'],['daily_returns']]
    return XLE_daily_returns_df

def spy_data(all_data):    
    SPY_daily_returns_df = all_data.loc[idx[:,'SPY'],['daily_returns']]
    return SPY_daily_returns_df
"""
def create_prepandemic_df(ticker_df_list,ticker_list):
    concat_df = pd.concat(ticker_df_list,axis=1, keys=ticker_list)
    return concat_df    

def create_prepandemic_mean_df(concat_df,ticker_type_list):
    mean_df=pd.DataFrame(concat_df.mean())
    mean_df=mean_df.reset_index()
    del mean_df['level_1']
    mean_df.columns=['Ticker','Mean']
    mean_df['Ticker_type']=ticker_type_list
    return mean_df

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
    
    
if __name__ =="__main__":
    
    user_choice = questionary.select("What would you like answers to\
                                 Choose 1 for: Which stock performed well in pre pandemic\
                                 Choose 2 for: Which etf performed well in pre pandemic\
                                 Choose 3 for: Which ticker performed better than SPY\
                                 Choose 4 for: Which stock performed inversely in pre pandemic\
                                 Choose 5 for: Which ETF performed inversely in pre pandemic?"
    ,choices = ["1","2","3","4","5"]).ask()


    
    ticker_list = ["AMZN", "RTH", "AMT", "IYR", "XOM", "XLE", "SPY"]
    ticker_type_list=['Stock','ETF','Stock','ETF','Stock','ETF','Index']
    POLYGON_API_KEY = 'JQfBpF3NpcYjuBdMiXeUr6q54XafY_pQ'
    all_data_df = date_ranges()
    ticker_df_list = []
    for tk in ticker_list:
        ticker_df_list.append(get_ticker_data_df(all_data_df,tk))
    if len(ticker_df_list) != len(ticker_list):
        print("ticker df list length not matching ticker list")
             
    prepandemic_df = create_prepandemic_df(ticker_df_list,ticker_list)
    prepandemic_mean_df = create_prepandemic_mean_df(prepandemic_df, ticker_type_list)
    display(prepandemic_mean_df)
    mysqlengine= create_sql_table(prepandemic_mean_df)
    if user_choice =="1":
        mytopstock = top_stock(mysqlengine)
        print(mytopstock)
    elif user_choice =="2":
        mytopetf = top_etf(mysqlengine)
        print(mytopetf)
    elif user_choice =="3":
        surspy=sur_spy(mysqlengine)
        print(surspy)
    elif user_choice =="4":
        mybottomstock = bottom_stock(mysqlengine)
        print(mybottomstock)
    elif user_choice =="5":
        mybottometf = bottom_etf(mysqlengine)
        print(mybottometf)
    else:
        print("User choice is not valid")
    
    
    
    
    
