import questionary
# from prepandemic import  top_stock
# from prepandemic import  top_etf
# from prepandemic import  sur_spy
# from prepandemic import  bottom_stock
# from prepandemic import  bottom_etf

from test import connection, top_stock, create_table




user_choice = questionary.select("What would you like answers to\
                                 Choose 1 for: Which stock performed well in pre pandemic\
                                 Choose 2 for: Which etf performed well in pre pandemic\
                                 Choose 3 for: Which ticker performed better than SPY\
                                 Choose 4 for: Which stock performed inversely in pre pandemic\
                                 Choose 5 for: Which ETF performed inversely in pre pandemic?"
,choices = ["1","2","3","4","5"]).ask()
create_table()
if user_choice =="1":
    
    top_stock()
# elif user_choice=="2":
#     top_etf()
# elif user_choice=="3":
#     sur_spy()
# elif user_choice=="4":
#     bottom_stock()
# elif user_choice=="5": 
#     botton_etf()  
else:
    print("Out of range")
