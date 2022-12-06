from PIL import Image
import streamlit as st
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

# Set page configurations - ALWAYS at the top
st.set_page_config(page_title="COVID portfolio analyzer",page_icon=":bar_chart:",layout="wide")


# Use local style.css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
        
local_css("./style/style.css")
        

# Title
with st.container():
    st.title("Dashboards")
    st.write("Select from the different time periods to highlight specific financial ratios of certain stocks/ETFs")
    st.write("---")

# Evaluation section
with st.container():    
    def get_prices(start_date,end_date,universe):
        data = pd.DataFrame()
        for t in tqdm(universe):
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
        data.t = pd.to_datetime(data.t, unit = 'ms')
        columns_name = {'t': 'time', 'o': 'Open', 'c': 'Close', 'h': 'High', 'l': 'Low', 'v': 'Volume'} 
        data= data.rename(columns = columns_name)
        data = data[['time','ticker','Open', 'Close','High', 'Low', 'Volume']]
        data = data.set_index(['time', 'ticker'])
        data["daily_returns"] = data['Close'].groupby('ticker').pct_change()
        data = data.dropna()
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

#Begin streamlit functionality
# Select a time-period section
with st.container():
    if __name__ =="__main__":
    #CLI OPTIONS    
            
        # 2 columns section:
        col1, col2 = st.columns([2, 3])
        with col1:
            start_date=""
            end_date=""
            st.subheader("Select a time-period:")
            user_choice_period = st.radio("",("pre-pandemic","pandemic","post-pandemic"),label_visibility="hidden")

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
                st.caption('Period is not valid.')
        with col2: st.empty()

# Select options from dropdown menu        
with st.container():
        # 2 columns section:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.write("###")       
            st.subheader("Select from the following options from the dropdown menu below:")
        
            user_choice_question = st.selectbox(
                                        "",
                ("Option 1: Which stock(s) performed well?",
                 "Option 2: Which ETF(s) performed well?",
                 "Option 3: Which ticker(s) performed better than SPY?",
                 "Option 4: Which stock(s) performed inversely?"
                 ,"Option 5: Which ETF(s) performed inversely?"),
                    label_visibility="hidden")

            st.write("You've selected the following - ", user_choice_question)

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
            #st.dataframe(std_df)

        #Mean Data    
            my_mean_df = create_mean_df(my_concat_df,ticker_type_list)
            #st.dataframe(my_mean_df)

        #SQL Engine    
            mysqlengine= create_sql_table(my_mean_df)


         #CLI OPTIONS   
            if user_choice_question =="Option 1: Which stock(s) performed well?":
                mytopstock = get_ticker_string(top_stock(mysqlengine))
                st.success(f'{mytopstock} is the top performing stock', icon="✅")
            elif user_choice_question =="Option 2: Which ETF(s) performed well?":
                mytopetf = get_ticker_string(top_etf(mysqlengine))
                st.success(f'{mytopetf} is the top performing ETF', icon="✅")
            elif user_choice_question =="Option 3: Which ticker(s) performed better than SPY?":
                surspy=sur_spy(mysqlengine)
                st.write('Ticker(s) that performed better than SPY is/are:', surspy)
            elif user_choice_question =="Option 4: Which stock(s) performed inversely?":
                mybottomstock = get_ticker_string(bottom_stock(mysqlengine))
                st.success(f'{mybottomstock} is the most inversely performing stock', icon="✅")
            elif user_choice_question =="Option 5: Which ETF(s) performed inversely?":
                mybottometf = get_ticker_string(bottom_etf(mysqlengine))
                st.success(f'{mybottometf} is the most inversely performing ETF', icon="✅")
            else:
                 st.success(f'User choice is not valid', icon="✅")
            with col2: st.empty()
        
        
        
# Choose a financial ratio from dropdown menu        
with st.container():
        # 2 columns section:
        col1, col2 = st.columns([2, 3])
        with col1:           
            st.write("###")
            st.subheader("Choose one of the following ratios below:")
        
            ratio_choice = st.selectbox("",("variance","co-variance","beta","mean","std-deviation","omega ratio"),label_visibility="hidden")
            st.write("You've selected the following ratio - ",ratio_choice)

            if ratio_choice == "variance":
                var_df = get_variance_per_ticker(ticker_df_list,ticker_list)
                st.write('Variance values are given below:',var_df)
            elif ratio_choice == "co-variance":
                covar_df = get_covariance_per_ticker(ticker_df_list,ticker_list)
                st.write('Co-variance values are given below:',covar_df)
            elif ratio_choice == "beta":
                covar_df = get_covariance_per_ticker(ticker_df_list,ticker_list)
                beta_df = get_beta_per_ticker(covar_df,ticker_df_list,ticker_list)
                st.write('Beta values are given below:',beta_df)
            elif ratio_choice == "mean":
                st.dataframe(my_mean_df)
            elif ratio_choice == "std-deviation":
                st.dataframe(std_df)
            elif ratio_choice == "omega ratio":
                st.empty()
            else:
                st.write(f'User choice is not valid')
                       