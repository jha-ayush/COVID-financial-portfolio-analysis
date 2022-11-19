#pip install questionary
import questionary
portfolio = questionary.select("what kind of investor are you?",choices = ["risk-averse", "risk-neutral", "risk-loving"]).ask()
top_stock = questionary.text("Which stock performed well in pre pandemic?").ask()
def top_stock():
    sel_port_max_mean="""select * from portfolio_mean where mean= (select max(mean) from portfolio_mean)"""
    max_mean=engine.execute(sel_port_max_mean)
    for row in max_mean:
        print(row)
        
    return
"""
"""
top_etf = questionary.text("Which etf performed well in pre pandemic?").ask()
def top_etf():
    sel_port_max_mean="""select * from portfolio_mean where mean= (select max(mean) from portfolio_mean)"""
    max_mean=engine.execute(sel_port_max_mean)
    for row in max_mean:
        print(row)
        
    return top_etf()

surpass_spy = questionary.text("Which ticker surpassed spy in pre pandemic?").ask()
def top_stock():
    sel_port_sur_spy="""select * from portfolio_mean where mean>0.0002883803029169555"""
    sur_spy=engine.execute(sel_port_sur_spy)
    for row in sur_spy:
        print(row)
        
    return top_stock()

inverse_stock = questionary.text("Which stock performed worse in pre pandemic?").ask()
def top_stock():
    sel_port_max_mean="""select * from portfolio_mean where mean= (select max(mean) from portfolio_mean)"""
    max_mean=engine.execute(sel_port_max_mean)
    for row in max_mean:
        print(row)
        
    return top_stock()

inverse_etf = questionary.text("Which etf performed worse in pre pandemic?").ask()
def bottom_etf():
    sel_port_min_mean="""select * from portfolio_mean where mean= (select min(mean) from portfolio_mean)"""
    min_mean=engine.execute(sel_port_min_mean)
    for row in max_mean:
        print(row)
        
    return bottom_etf()


