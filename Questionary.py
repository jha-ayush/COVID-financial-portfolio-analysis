import questionary
#import import_ipynb
#import prepandemic_financial_portfolio_analyzer.ipynb as pre

user_choice = questionary.select("What would you like answers to\
                                 Choose 1 for: Which stock performed well in pre pandemic\
                                 Choose 2 for: Which etf performed well in pre pandemic\
                                 Choose 3 for: Which ticker performed better than SPY\
                                 Choose 4 for: Which stock performed inversely in pre pandemic\
                                 Choose 5 for: Which ETF performed inversely in pre pandemic?"
,choices = ["1","2","3","4","5"]).ask()

if user_choice =="1":
    pre.top_stock()
elif user_choice=="2":
    pre.top_etf()
elif user_choice=="3":
    pre.sur_spy()
elif user_choice=="4":
    pre.bottom_stock()
elif user_choice=="5": 
    pre.botton_etf()          
