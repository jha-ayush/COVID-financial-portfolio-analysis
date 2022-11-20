from functions import *
import pandas as pd
#import fire

tech_list = ['AMZN','RTH']
start_date = "2017-03-01"
end_date = "2020-02-29"
POLYGON_API_KEY = 'JQfBpF3NpcYjuBdMiXeUr6q54XafY_pQ'

def risk_loving():
    POLYGON_API_KEY = 'JQfBpF3NpcYjuBdMiXeUr6q54XafY_pQ'
    all_data = get_prices(start_date=start_date, end_date=end_date, universe=tech_list)
    return all_data


def monte_carlo():
    thirty_year_simulation = MCSimulation(
    portfolio_data=tech_list,
    weights=[0.60, 0.40],
    num_simulation=500,
    num_trading_days=252*30,)    
    thirty_year_simulation.plot_simulation()


#if __name__ =="__main__":


    
risk_loving()
monte_carlo()

def create_std_df(concat_df,ticker_type_list):
    std_df=pd.DataFrame(concat_df.std())
    std_df=std_df.reset_index()
    del std_df['level_1']
    std_df.columns=['Ticker','Mean']
    std_df['Ticker_type']=ticker_type_list
    return std_df

def create_var(concat_df)
    variance=concat_df.var()
    return create_var

def create_covar(concat_df)
    covariance = concat_df['AMZN'].cov(concat_df['SPY'])
    covariance = concat_df['RTH'].cov(concat_df['SPY'])
    covariance = concat_df['IYR'].cov(concat_df['SPY'])
    covariance = concat_df['AMT'].cov(concat_df['SPY'])
    covariance = concat_df['XOM'].cov(concat_df['SPY'])
    covariance = concat_df['XLE'].cov(concat_df['SPY'])


def beta(concat_df)


    return beta

def sharpe_ratio(concat_df)



    return sharpe_ratio

