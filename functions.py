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
from watermark import watermark
import datetime
from time import sleep
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
from pytz import timezone
import pyfolio as pf
from IPython.display import display
import matplotlib
import re
'https://api.polygon.io/v2/aggs/ticker/AMZN/range/1/day/2021-03-01/2022-03-01?adjusted=true&apiKey=hpeq4ZPUPErMkP2WZv5pNhAtO002i4ZF'
def get_prices(start_date,end_date,universe):
    data = pd.DataFrame()
    # end_at = datetime.datetime.now() 
    # begin_from = end_at + datetime.timedelta(days=-5000)
    for t in tqdm(universe):
        #print(t)
        #print(start_date)
        #print(end_date)
        #print(len(data))
        # for start in pd.date_range(start = begin_from, end = end_at,normalize=True,freq = '88D'):
        #     end = start + datetime.timedelta(days = 88)
        #     end = str(int((end - datetime.datetime(1970,1,1)).total_seconds()))
        #     start = str(int((start - datetime.datetime(1970,1,1)).total_seconds()))
        try:
            r = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{t}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}')
        except json.JSONDecodeError:
            pass
        try:
            
            temp_data = pd.DataFrame(r.json()['results'])
            #print(temp_data)
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
    #print(data)
    data.t = pd.to_datetime(data.t, unit = 'ms')
    columns_name = {'t': 'time', 'o': 'Open', 'c': 'Close', 'h': 'High', 'l': 'Low', 'v': 'Volume'} 
    data= data.rename(columns = columns_name)
    data = data[['time','ticker','Open', 'Close','High', 'Low', 'Volume']]
    data = data.set_index(['time', 'ticker'])
    data["daily_returns"] = data['Close'].groupby('ticker').pct_change()
    data = data.dropna()
    #data.to_csv(file_name, index = False)
    return data
    

def date_ranges(start_date,end_date,ticker_list):
    all_data = get_prices(start_date=start_date, end_date=end_date, universe=ticker_list)    
    return all_data

def get_ticker_data_df(all_data, ticker_symbol):
    idx = pd.IndexSlice
    daily_returns_df = all_data.loc[idx[:,ticker_symbol],['daily_returns']]
    return daily_returns_df

def create_concat_df(ticker_df_list,ticker_list):
    concat_df = pd.concat(ticker_df_list,axis=1, keys=ticker_list)
    return concat_df    

#Mean Function
def create_mean_df(concat_df,ticker_type_list):
    mean_df=pd.DataFrame(concat_df.mean())
    mean_df=mean_df.reset_index()
    del mean_df['level_1']
    mean_df.columns=['Ticker','Mean']
    mean_df['Ticker_type']=ticker_type_list
    return mean_df


#Standard Deviation Function
def create_std_df(concat_df,ticker_type_list):
    std_df=pd.DataFrame(concat_df.std())
    std_df=std_df.reset_index()
    del std_df['level_1']
    std_df.columns=['Ticker','STD']
    std_df['Ticker_type']=ticker_type_list
    return std_df

#Variance Function
def get_var(concat_df,column):
    variance=concat_df[column].var()
    return vaariance 

#Database Connection
def create_connection():
    database_connection_string = 'sqlite:///'
    engine = sqlalchemy.create_engine(database_connection_string)
    #print(engine.table_names())
    return engine

#SQL Table Creation
def create_sql_table(mean_df):
    engine = create_connection()
    mean_df.to_sql('portfolio_mean',engine)
    return engine
    
 #Top Stock Function   
def top_stock(engine):
    sel_max_mean="""select Ticker from portfolio_mean where mean= (select max(Mean) from portfolio_mean where Ticker_type='Stock')"""
    max_mean=list(engine.execute(sel_max_mean))
    if len(max_mean)==1:
        return str(max_mean[0])
    else:
        print("Check code")

#Bottom Stock Function
def bottom_stock(engine):
    sel_min_mean="""select Ticker from portfolio_mean where mean= (select min(mean) from portfolio_mean where Ticker_type='Stock')"""
    min_mean=list(engine.execute(sel_min_mean))
    if len(min_mean)==1:
        return str(min_mean[0])
    else:
        print("Check code")

        
#Top ETF Function        
def top_etf(engine):
    sel_port_max_mean="""select Ticker from portfolio_mean where mean= (select max(Mean) from portfolio_mean where Ticker_type='ETF')"""
    max_mean=list(engine.execute(sel_port_max_mean))
    if len(max_mean)==1:
        return str(max_mean[0])
    else:
        print("Check code")

        
#Bottom ETF Function        
def bottom_etf(engine):
    sel_port_min_mean="""select Ticker from portfolio_mean where mean=(select min(mean) from portfolio_mean where Ticker_type='ETF')"""
    min_mean=list(engine.execute(sel_port_min_mean))
    if len(min_mean)==1:
        return str(min_mean[0])
    else:
        print("Check code")

#Surpass SPY Function        
def sur_spy(engine):
    sel_port_sur_spy="""select b.Ticker from portfolio_mean a, portfolio_mean b where a.Mean<b.Mean and a. Ticker='SPY'"""
    sur_spy=list(engine.execute(sel_port_sur_spy))
    return pd.DataFrame(sur_spy, columns = ["Best Performers"])


def get_ticker_string(str):
    match = re.search(r'\(\'([A-Z]+)\',\)', str)
    if match:
        return match.group(1)
    else:
        print("RE pattern match failed. Found str : {str}")

        
#Variance Function        
def get_variance_per_ticker(ticker_df_list,ticker_list):
    var_dict = {} 
    for idx in range(len(ticker_list)):
        var_dict[ticker_list[idx]]=ticker_df_list[idx]['daily_returns'].var()
    return pd.DataFrame(var_dict, index=[0])

#Covariance Function
def get_covariance_per_ticker(ticker_df_list,ticker_list):
    covar_dict = {}
    # Find index of SPY in ticker_list
    try:
        spy_idx=ticker_list.index("SPY")
    except:
        print("Cannot find SPY in ticker list. Cannot calculate Covariance based on SPY")
        return
        
    # get dataframe for SPY based on index
    SPY_df = ticker_df_list[spy_idx].reset_index(level = 1, drop= True)
    for idx in range(len(ticker_list)):
        covar_dict[ticker_list[idx]]=ticker_df_list[idx].reset_index(level = 1, drop= True)['daily_returns'].cov(SPY_df['daily_returns'])
    return pd.DataFrame(covar_dict, index=[0])
                                                    
#Beta Function                                                    
def get_beta_per_ticker(covar_df,ticker_df_list,ticker_list):
    beta_dict ={}
    try:
        spy_idx=ticker_list.index("SPY")
    except:
        print("Cannot find SPY in ticker list. Cannot calculate Covariance based on SPY")
        return
        
    # get dataframe for SPY based on index
    SPY_df = ticker_df_list[spy_idx]
    SPY_var = float(SPY_df['daily_returns'].var())
    for idx in range(len(ticker_list)):
        tk = ticker_list[idx]
        beta_dict[tk] = float(covar_df.iloc[0,idx])/SPY_var
    return pd.DataFrame(beta_dict, index=[0])                                        
                                                    
                                                    
                                                    
if __name__ =="__main__":
#CLI OPTIONS    
    user_choice_period = questionary.select("select a period?",choices = ["pre-pandemic","pandemic","post-pandemic"]).ask()
    start_date=""
    end_date=""
    if user_choice_period == "pre-pandemic":
        start_date = "2017-03-01"
        end_date = "2020-02-29"
    elif user_choice_period == "pandemic":       
        start_date = "2020-03-01"
        end_date = "2021-02-28"
    elif user_choice_period == "post-pandemic":
        start_date = "2021-03-01"
        end_date = "2022-03-01"
    else:
        print("period not valid")
    answers = "What would you like answers to \n\
                                 Choose 1 for: Which stock performed well \n\
                                 Choose 2 for: Which etf performed well \n\
                                 Choose 3 for: Which ticker performed better than SPY \n\
                                 Choose 4 for: Which stock performed inversely \n\
                                 Choose 5 for: Which ETF performed inversely?"
    user_choice_question = questionary.select(answers
    ,choices = ["1","2","3","4","5"]).ask()

#Ticker List    
    ticker_list = ["AMZN", "RTH", "AMT", "IYR", "XOM", "XLE", "SPY"]
    ticker_type_list=['Stock','ETF','Stock','ETF','Stock','ETF','Index']
    POLYGON_API_KEY = 'JQfBpF3NpcYjuBdMiXeUr6q54XafY_pQ'
    
#All Ticker Data    
    all_data_df = date_ranges(start_date,end_date,ticker_list)
    #display(all_data_df)
    
#List of Data Frames for Individual Tickers     
    ticker_df_list = []
    for tk in ticker_list:
        ticker_df_list.append(get_ticker_data_df(all_data_df,tk))
        
    if len(ticker_df_list) != len(ticker_list):
        print("ticker df list length not matching ticker list")
        
        
#Concatenated Data             
    my_concat_df = create_concat_df(ticker_df_list,ticker_list)
    #display(my_concat_df)
    
#STD Data
    std_df = create_std_df(my_concat_df, ticker_type_list)
    #display(std_df)
    
#Mean Data    
    my_mean_df = create_mean_df(my_concat_df,ticker_type_list)
    #display(my_mean_df)
    
#SQL Engine    
    mysqlengine= create_sql_table(my_mean_df)
    
    
 #CLI OPTIONS   
    if user_choice_question =="1":
        mytopstock = get_ticker_string(top_stock(mysqlengine))
        print(f'{mytopstock} is top performing stock')
    elif user_choice_question =="2":
        mytopetf = get_ticker_string(top_etf(mysqlengine))
        print(f'{mytopetf} is top performing ETF')
    elif user_choice_question =="3":
        surspy=sur_spy(mysqlengine)
        print(f'{str(surspy)} \nPerformed better than SPY')
    elif user_choice_question =="4":
        mybottomstock = get_ticker_string(bottom_stock(mysqlengine))
        print(f'{mybottomstock} is worst performing Stock')
    elif user_choice_question =="5":
        mybottometf = get_ticker_string(bottom_etf(mysqlengine))
        print(f'{mybottometf} is worst performing ETF')
    else:
        print('User choice is not valid')
        
        
#Variance
    var_df = get_variance_per_ticker(ticker_df_list,ticker_list)
    display(var_df)
    
    
#Covariance    
    covar_df = get_covariance_per_ticker(ticker_df_list,ticker_list)
    #display(covar_df)
    
    
#Beta    
    beta_df = get_beta_per_ticker(covar_df,ticker_df_list,ticker_list)
    #display(beta_df)
    
    

    
    
    
    
    
    
