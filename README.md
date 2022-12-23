# COVID Portfolio Analysis
> Business [pitch](https://share.synthesia.io/606a3c1a-5dc5-4f5e-b62c-714122d22ebd "Avatar pitch")

> Executive [summary](https://github.com/jha-ayush/finance_portfolio_analyzer/blob/main/exec_summary.md "Executive summary")

> Streamlit web [app](https://jha-ayush-finance-portfolio-analyzer-home-dnt6yf.streamlit.app/ "Portfolio analyzer web app")

> Project [presentation](https://docs.google.com/presentation/d/1h6WeGVXbMMQkdrFOkK9d-qfRLPB0UTQduO6VTPxZbtA/edit?usp=sharing "Portfolio Analyzer")

### Launch app on localhost:
- `git clone` main [branch](https://github.com/jha-ayush/finance_portfolio_analyzer "Main Branch")
- Navigate to the local directory in Terminal
- Switch to `dev` environment `conda activate dev`
- `pip install -r requirements.txt`
- Navigate to `functionality_files` directory in Terminal
- Enter `streamlit run Home.py` to launch localhost app

#### Environment setup
To install all required packages
- `pip install -r requirements.txt`

#### Analysis
To analyze each sector and time period, we used a variety of metrics and statistics, such as Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio.

#### Results

##### Pre-Pandemic Results:
As expected most of the sectors were experiencing a growth environment. This was consistent with the rest of the economy at large. We found the Technology sector to be the best performing sector, as a whole as the Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio were highest in this sector. It is important to note, in particular, investing in AMT (American Towers) would have yielded the biggest returns for the pre-pandemic period as it had the absolute highest ratios. We found the worst performing sector to be the Energy sector, with negative values for the aforementioned ratios.

##### Pandemic Results:
With a large portion of Americans at home and the ease of online shopping, the Consumer Goods sector was the first to recover from the initial shock of the economic slowdown caused by the Pandemic. We found the Technology sector to be the best performing sector, as the Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio were highest in this sector. We found the worst performing sector to be the Real Estate sector, with the lowest values for the aforementioned ratios.

##### Post-Pandemic Results:
We found the Energy sector to be the best perfoming sector, as the Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio were by far the highest in this sector. Specifically, investing in XOM (Exxon Mobile) would have yielded the greatest returns for the post-pandemic period. We found the worst performing sector to be the Technology sector, with the largest negative values for the aforementioned ratios.


#### Technical notes

##### Project Description/Outline
We used [polygon.io](https://polygon.io/ "Polygon.io") to make [RESTful API](https://polygon.io/docs/stocks/getting-started "Polygon Stocks API Docs") calls using their [Starter paywall](https://polygon.io/pricing "Polygon pricing")


### Team members
- **Christine Pham**  -  `cpham35`
- **Kranthi Mitta**  -  `kranthicmitta`
- **Kevin Herndon**  -  `Kevtech577`
- **Ben Smookler**  -  `BenSmook`
- **Ayush Jha**  -  `jha-ayush`

