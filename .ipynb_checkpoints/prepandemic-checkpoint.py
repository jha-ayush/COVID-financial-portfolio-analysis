#!/usr/bin/env python
# coding: utf-8

# # Portfolio Analyzer

# In[86]:


#pip install polygon-api-client


# In[86]:


#pip install polygon-api-client


# In[ ]:


#from polygon import RESTClient


# In[3]:


#import the necessary modules
import pandas as pd
import numpy as np
#questionary
from pathlib import Path
import fire
import questionary
#API
import os
import json
import requests
from dotenv import load_dotenv
from MCForecastTools import MCSimulation



# In[4]:





# In[5]:


POLYGON_API_KEY ='enZp2AUpH4pGXJJuQ1CbjdVXJIsBFBEl'


# In[6]:


# Load .env enviroment variables into the notebook
#load_dotenv()


# In[7]:


# Get the API key from the environment variable and store as Python variable
#polygon_api_key = os.getenv("POLYGON_API_KEY")

# Using the type funcion, confirm that the Nasdaq API key is available for use in the notebook
#type(polygon_api_key)


# In[8]:


ticker_list = ["AMZN", "RTH", "AMT", "IYR", "XOM", "XLE", "SPY"]


# In[9]:


import requests
import datetime
from time import sleep
from tqdm import tqdm
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


# In[10]:


#f"https://api.polygon.io/v2/aggs/ticker/{t}/range/1/day/{start_date}/{end_date}?apiKey=rHtIrGbGhJY6umnXSqp6hYgTM3XnHI2_"


# In[11]:


# Create `start_date` and `end_date` variables for the period before the pandemic
start_date = "2017-03-01"
end_date = "2020-03-01"
all_data = get_prices(start_date=start_date, end_date=end_date, universe=ticker_list)
#example
#big_mac_usa = "https://data.nasdaq.com/api/v3/datasets/ECONOMIST/BIGMAC_USA?start_date=" + start_date + "&end_date=" + end_date + "&api_key=" + nasdaq_api_key


# In[12]:


all_data.index


# In[13]:


idx = pd.IndexSlice


# In[14]:


AMZN_daily_returns_df = all_data.loc[idx[:,'AMZN'],['daily_returns']]
AMZN_daily_returns_df


# In[15]:


RTH_daily_returns_df = all_data.loc[idx[:,'RTH'],['daily_returns']]
RTH_daily_returns_df


# In[16]:


AMT_daily_returns_df = all_data.loc[idx[:,'AMT'],['daily_returns']]
AMT_daily_returns_df


# In[17]:


IYR_daily_returns_df = all_data.loc[idx[:,'IYR'],['daily_returns']]
IYR_daily_returns_df


# In[18]:


XOM_daily_returns_df = all_data.loc[idx[:,'XOM'],['daily_returns']]
XOM_daily_returns_df


# In[19]:


XLE_daily_returns_df = all_data.loc[idx[:,'XLE'],['daily_returns']]
XLE_daily_returns_df


# In[20]:


SPY_daily_returns_df = all_data.loc[idx[:,'SPY'],['daily_returns']]
SPY_daily_returns_df


# In[21]:


tech_daily_returns = pd.concat([AMZN_daily_returns_df, RTH_daily_returns_df], keys=["AMZN","RTH"])
tech_daily_returns


# In[22]:


RE_daily_returns = pd.concat([AMT_daily_returns_df, IYR_daily_returns_df], keys=["AMT","IYR"])
RE_daily_returns


# In[23]:


energy_daily_returns = pd.concat([XOM_daily_returns_df, XLE_daily_returns_df], keys=["XOM","XLE"])
energy_daily_returns


# In[24]:


#Display all sectors of the stock/ETF dataframes
dfT_style = tech_daily_returns.style.set_table_attributes("style='display:inline; margin-right:20px;'").set_caption("Tech")
dfR_style = RE_daily_returns.style.set_table_attributes("style='display:inline'").set_caption("Real Estate")
dfE_style = energy_daily_returns.style.set_table_attributes("style='display:inline'").set_caption("Energy")


display_html(dfT_style._repr_html_() + dfR_style._repr_html_() + dfE_style._repr_html_(), raw=True)


# ### A) Analyzing Each Stock and ETF Individually
# 

# In[121]:


import warnings
warnings.filterwarnings("ignore")


# In[122]:


from pytz import timezone

from time import sleep
import numpy as np
import pyfolio as pf
import sqlalchemy


# In[123]:


Pandemic_prices_df = pd.concat([AMZN_daily_returns_df, RTH_daily_returns_df, AMT_daily_returns_df, IYR_daily_returns_df, XOM_daily_returns_df, XLE_daily_returns_df, SPY_daily_returns_df],axis=1, keys=["AMZN","RTH","AMT","IYR","XOM","XLE","SPY"])


# In[150]:


pandemic_std=pd.DataFrame(Pandemic_prices_df.std())
pandemic_std=pandemic_std.reset_index()
del pandemic_std['level_1']
pandemic_std.rename({'level_0': 'Ticker', 0: 'STD'}, axis=1, inplace=True)
pandemic_std['ticker_type']=['Stock','ETF','Stock','ETF','Stock','ETF','Index']
pandemic_std


# In[170]:


pandemic_mean=pd.DataFrame(Pandemic_prices_df.std())
pandemic_mean=pandemic_mean.reset_index()
del pandemic_mean['level_1']
pandemic_mean.columns=['Ticker','Mean']
pandemic_mean['Ticker_type']=['Stock','ETF','Stock','ETF','Stock','ETF','Index']
pandemic_mean


# In[171]:


database_connection_string = 'sqlite:///'


# In[172]:


engine = sqlalchemy.create_engine(database_connection_string)


# In[173]:


engine.table_names()


# In[174]:


pandemic_mean.to_sql('portfolio_mean',engine)


# In[175]:


engine.table_names()


# In[176]:


del_spy_mean = """delete from portfolio_mean where mean=0.000288"""
engine.execute(del_spy_mean)


# In[202]:


def top_stock():
    sel_port_max_mean="""select Ticker from portfolio_mean where mean= (select max(Mean) from portfolio_mean where Ticker_type='Stock')"""
    max_mean=engine.execute(sel_port_max_mean)
    for row in max_mean:
        print(row)


# In[203]:


top_stock()


# In[204]:


def bottom_stock():
    sel_port_min_mean="""select Ticker from portfolio_mean where mean= (select min(mean) from portfolio_mean where Ticker_type='Stock')"""
    min_mean=engine.execute(sel_port_min_mean)
    for row in min_mean:
        print(row)


# In[180]:


bottom_stock()


# In[205]:


def top_etf():
    sel_port_max_mean="""select Ticker from portfolio_mean where mean= (select max(Mean) from portfolio_mean where Ticker_type='ETF')"""
    max_mean=engine.execute(sel_port_max_mean)
    for row in max_mean:
        print(row)


# In[206]:


top_etf()


# In[207]:


def bottom_etf():
    sel_port_min_mean="""select Ticker from portfolio_mean where mean=(select min(mean) from portfolio_mean where Ticker_type='ETF')"""
    min_mean=engine.execute(sel_port_min_mean)
    for row in min_mean:
        print(row)


# In[208]:


bottom_etf()


# In[223]:


def sur_spy():
    sel_port_sur_spy="""select Ticker from portfolio_mean where Mean>0.009506"""
    sur_spy=engine.execute(sel_port_sur_spy)
    for row in sur_spy:
        print(row)


# In[224]:


sur_spy()


# In[199]:


Pandemic_prices_df


# In[ ]:


#Summary statistics for AMZN stock using .std() and .mean()
display(AMZN_daily_returns_df.std())
display(AMZN_daily_returns_df.mean())


# In[ ]:


#Summary statistics for RTH stock using .std() and .mean()
RTH_daily_returns_df.std()
RTH_daily_returns_df.mean()


# In[ ]:


#Summary statistics for AMT stock using .std() and .mean()
AMT_daily_returns_df.std()
AMT_daily_returns_df.mean()


# In[ ]:


#Summary statistics for IYR stock using .std() and .mean()
IYR_daily_returns_df.std()
IYR_daily_returns_df.mean()


# In[ ]:


#Summary statistics for XOM stock using .std() and .mean()
XOM_daily_returns_df.std()
XOM_daily_returns_df.mean()


# In[ ]:


#Summary statistics for XLE stock using .std() and .mean()
XLE_daily_returns_df.std()
XLE_daily_returns_df.mean()


# In[ ]:


Pandemic_prices_df.describe()


# In[ ]:


#Summary statistics for AMZN using .describe()
AMZN_daily_returns_df.describe()


# In[ ]:


#Summary statistics for RTH using .describe()
RTH_daily_returns_df.describe()


# In[ ]:


#Summary statistics for AMT using .describe()
AMT_daily_returns_df.describe()


# In[ ]:


#Summary statistics for IYR using .describe()
IYR_daily_returns_df.describe()


# In[ ]:


#Summary statistics for XOM using .describe()
XOM_daily_returns_df.describe()


# In[ ]:


#Summary statistics for XLE using .describe()
XLE_daily_returns_df.describe()


# In[ ]:


Pandemic_var=Pandemic_prices_df.var()
Pandemic_var


# In[ ]:


# Variance Of Amzn
AMZN_var=AMZN_daily_returns_df.var()
AMZN_var


# In[ ]:


# Variance For RTH
RTH_var=RTH_daily_returns_df.var()
RTH_var


# In[ ]:


# Variance Of IYR
IYR_var=IYR_daily_returns_df.var()
IYR_var


# In[ ]:


# Variance Of AMT
AMT_var=AMT_daily_returns_df.var()
AMT_var


# In[ ]:


# Variance Of XOM
XOM_var=XOM_daily_returns_df.var()
XOM_var


# In[ ]:


# Variance Of XLE
XLE_var=XLE_daily_returns_df.var()
XLE_var


# In[109]:


# Covariance for Each Stock and ETF
AMZN_RTH_Cov=AMZN_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns'])
AMZN_RTH_Cov


# In[ ]:


# Covariance for Each Stock and ETF
AMT_IYR_Cov=AMT_daily_returns_df['daily_returns'].cov(IYR_daily_returns_df['daily_returns'])
AMT_IYR_Cov


# In[ ]:


# Covariance for Each Stock and ETF
XOM_XLE_Cov=XOM_daily_returns_df['daily_returns'].cov(XLE_daily_returns_df['daily_returns'])
XOM_XLE_Cov


# In[ ]:


year_trading_days = 252


# In[ ]:


Pandemic_prices_ann_ret=Pandemic_prices_df.mean()*year_trading_days
Pandemic_prices_ann_ret


# In[ ]:


# Annualized returns of RTH
RTH_Annual_Ret = RTH_daily_returns_df.mean()*252
RTH_Annual_Ret


# In[ ]:


# Annualized returns of IYR
IYR_Annual_Ret = IYR_daily_returns_df.mean()*252
IYR_Annual_Ret


# In[ ]:


# Annualized returns of XLE
XLE_Annual_Ret = XLE_daily_returns_df.mean()*252
XLE_Annual_Ret


# In[ ]:


Pandemic_prices_ann_std=Pandemic_prices_df.std()*np.sqrt(year_trading_days)
Pandemic_prices_ann_std


# In[ ]:


# Annualized std dev of RTH
annual_std_dev_RTH = RTH_daily_returns_df.std() * np.sqrt(year_trading_days)
annual_std_dev_RTH


# In[ ]:


# Annualized std dev of IYR
annual_std_dev_IYR = IYR_daily_returns_df.std() * np.sqrt(year_trading_days)
annual_std_dev_IYR


# In[ ]:


# Annualized std dev of XLE
annual_std_dev_XLE = XLE_daily_returns_df.std() * np.sqrt(year_trading_days)
annual_std_dev_XLE


# In[ ]:


Pandemic_prices_ann_ret/Pandemic_prices_ann_std


# In[ ]:


#Sharpe ratio for each stock and ETF 
Sharpe_RTH = RTH_Annual_Ret/annual_std_dev_RTH
Sharpe_RTH


# In[ ]:


#Sharpe ratio for each stock and ETF 
Sharpe_IYR = IYR_Annual_Ret/annual_std_dev_IYR
Sharpe_IYR 


# In[ ]:


#Sharpe ratio for each stock and ETF 
Sharpe_XLE = XLE_Annual_Ret/annual_std_dev_XLE
Sharpe_XLE


# In[ ]:


Pandemic_prices_beta_AMZN=AMZN_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns']) / SPY_daily_returns_df["daily_returns"].var()
Pandemic_prices_beta


# In[114]:


# Calculate betas of AMZN
AMZN_beta = AMZN_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns'])/SPY_daily_returns_df['daily_returns'].var()
# Display the beta of all stocks and ETFS
AMZN_beta


# In[116]:


# Calculate betas of RTH
RTH_beta = RTH_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns'])/SPY_daily_returns_df['daily_returns'].var()
# Display the beta of all stocks and ETFS
RTH_beta


# In[117]:


# Calculate betas of AMT
AMT_beta =AMT_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns'])/SPY_daily_returns_df['daily_returns'].var()
# Display the beta of all stocks and ETFS
AMT_beta


# In[118]:


# Calculate betas of IYR
IYR_beta = IYR_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns'])/SPY_daily_returns_df['daily_returns'].var()
# Display the beta of all stocks and ETFS
IYR_beta


# In[119]:


# Calculate betas of XOM
XOM_beta = XOM_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns'])/SPY_daily_returns_df['daily_returns'].var()
# Display the beta of all stocks and ETFS
XOM_beta


# In[120]:


# Calculate betas of XLE 
XLE_beta = XLE_daily_returns_df['daily_returns'].cov(SPY_daily_returns_df['daily_returns'])/SPY_daily_returns_df['daily_returns'].var()
# Display the beta of all stocks and ETFS
XLE_beta


# In[ ]:


result = pf.create_returns_tear_sheet(AMZN_daily_returns_df.reset_index(level = 1,drop = True).daily_returns,
                                           return_fig=True)
#result.savefig("amzn_prepan_tearsheet.png", format = "png")


# In[ ]:


result = pf.create_returns_tear_sheet(RTH_daily_returns_df.reset_index(level = 1,drop = True).daily_returns,
                                           return_fig=True)
#result.savefig("RTH_prepan_tearsheet.png", format = "png")


# In[ ]:


result = pf.create_returns_tear_sheet(AMT_daily_returns_df.reset_index(level = 1,drop = True).daily_returns,
                                           return_fig=True)
#result.savefig("amt_prepan_tearsheet.png", format = "png")


# In[ ]:


result = pf.create_returns_tear_sheet(IYR_daily_returns_df.reset_index(level = 1,drop = True).daily_returns,
                                           return_fig=True)
#result.savefig("iyr_prepan_tearsheet.png", format = "png")


# In[ ]:


result = pf.create_returns_tear_sheet(XOM_daily_returns_df.reset_index(level = 1,drop = True).daily_returns,
                                           return_fig=True)
#result.savefig("xom_prepan_tearsheet.png", format = "png")


# In[ ]:


result = pf.create_returns_tear_sheet(XLE_daily_returns_df.reset_index(level = 1,drop = True).daily_returns,
                                           return_fig=True)
#result.savefig("xle_prepan_tearsheet.png", format = "png")


# In[ ]:


result = pf.create_returns_tear_sheet(SPY_daily_returns_df.reset_index(level = 1,drop = True).daily_returns,
                                           return_fig=True)
#result.savefig("spy_prepan_tearsheet.png", format = "png")


# In[ ]:


# Calculate alphas of AMZN
Alpha = R – Rf – beta (Rm-Rf)
AMZN_Alpha = R – Rf – AMZN_beta (Rm-Rf)
# Display the alphas of all stocks and ETFS
AMZN_Alpha


# In[ ]:


# Calculate alphas of RTH
RTH_Alpha = R – Rf – RTH_beta (Rm-Rf)
# Display the alphas of all stocks and ETFS
RTH_Alpha


# In[ ]:


# Calculate alphas of AMT
AMT_Alpha = R – Rf – AMT_beta (Rm-Rf)
# Display the alphas of all stocks and ETFS
AMT_Alpha


# In[ ]:


# Calculate alphas of IYR
IYR_Alpha = R – Rf – IYR_beta (Rm-Rf)
# Display the alphas of all stocks and ETFS
IYR_Alpha


# In[ ]:


# Calculate alphas of XOM
XOM_Alpha = R – Rf – XOM_beta (Rm-Rf)
# Display the alphas of all stocks and ETFS
XOM_Alpha


# In[ ]:


# Calculate alphas of XLE 
XLEZZ_Alpha = R – Rf – XLE_beta (Rm-Rf)
XLEZZ_Alpha


# ### A) Analyzing What Would Happen To A Portfolio in Each Sector For the Period Before the Pandemic

# In[ ]:


import questionary


# In[ ]:


#Questionary SQL
#what kind of investor are you (risk-averse, risk-neutral, risk loving)?

#Which company performed well in pre pandemic?
#Which ETF performed well in pre pandemic?
#Which ticker performed better than SPY?
#Which company performed inversely in pre pandemic?
#Which ETF performed inversely in pre pandemic?


# In[ ]:





# In[ ]:


#Portfolio Returns for Tech: use (portfolio_return = weightAMZN * meanAMZN + weightRTH * meanRTH)


# In[ ]:


#Portfolio Returns for Real Estate: use (portfolio_return = weightAMT * meanAMT + weightIYR * meanIYR)


# In[ ]:


#Portfolio Returns for Energy: use (portfolio_return = weightXOM * meanXOM + weightXLE * meanXLE)


# In[ ]:


# Using the Pandas var function, calculate the covariance of the S&P 500 using tech portfolio returns information
# The ETF SPY will represent the market


# In[ ]:


# Using the Pandas var function, calculate the covariance of the S&P 500 using Real Estate portfolio returns information
# The ETF SPY will represent the market


# In[ ]:


# Using the Pandas var function, calculate the covariance of the S&P 500 using Energy portfolio returns information
# The ETF SPY will represent the market


# In[ ]:


#Calculate the Portfolio Standard Deviation for Tech: use (weightAMZN^2 * MeanAMZN^2 + weightRTH^2 * MeanRTH^2 + 2*weightAMZN*weightRTH*stdevAMZN*stdevRTH*covAMZN,RTH)


# In[ ]:


#Calculate the Portfolio Standard Deviation for Real Estate


# In[ ]:


#Calculate the Portfolio Standard Deviation for Energy


# In[ ]:


# Using the Pandas rolling function in conjunction with the var function, 
# calculate the 30-day rolling variance for the S&P 500 using tech daily returns information

# Visualize the 30-day rolling variance of the S&P 500
# Be sure to adjust the figure size and add a title


# In[ ]:


#Monte Carlo Simulation


# In[ ]:


#Box and Whisker Plot


# In[ ]:


#HVPlot


# In[ ]:


#bar plot comparing returns of all sectors 


# In[ ]:


#bar plot comparing returns of all portfolio


# In[ ]:




