# Financial Portfolio Analysis
> [Portfolio Analyzer pitch](https://share.synthesia.io/606a3c1a-5dc5-4f5e-b62c-714122d22ebd "Avatar pitch")


> [Project presentation](https://docs.google.com/presentation/d/1h6WeGVXbMMQkdrFOkK9d-qfRLPB0UTQduO6VTPxZbtA/edit?usp=sharing "Portfolio Analyzer")

We built a portfolio analyzer tear sheet to view financial market behaviors of specific investment stocks & ETFs from FY 2017-2022 to assess the impacts of pre-COVID and post-COVID timelines. We are going to compare the data against the S&P500 index.


### Project Description/Outline
We will use [polygon.io](https://polygon.io/ "Polygon.io") to make [RESTful API](https://polygon.io/docs/stocks/getting-started "Polygon Stocks API Docs") calls using their [Starter paywall](https://polygon.io/pricing "Polygon pricing") with the following features below:

- <sub>$29/month</sub>
- <sub>15-minute delayed data</sub>
- <sub>5 years max historical data</sub>
- <sub>100% market coverage</sub>

General to dos:
- pull data from API's
- calculate returns
- variance
- covariance
- alpha
- beta
- Sharpe ratio
- mean
- summary statistics
- questionary with SQL
- Dashboard deployment

### Team members
- **Christine Pham**  -  `cpham35`
- **Kranthi Mitta**  -  `kranthicmitta`
- **Kevin Herndon**  -  `Kevtech577`
- **Ben Smookler**  -  `BenSmook`
- **Ayush Jha**  -  `jha-ayush`

### Research Questions to Answer
- As a user, I want to be able to access the portfolio online online
- As a user, I want access to visualization data for at least 3-5 years in the past from the current time period
- As a user, I want access to visualization data for only the stocks in the portfolio
- As a user, I want access to dashboard to assess the movement of the stocks
- As a user, I want to be able to compare the portfolio against the S&P500 index
- As a user, I want access to visualization data for multiple scenarios of investment types
- As a user, I would like suggestions on the following tracks (most risky to most conservative) for the portfolio


### pip packages

- watermark
- warnings
- polygon-api-client
- pandas
- numpy
- numba
- pathlib
- fire
- questionary
- dotenv
- streamlit
- streamlit-lottie
- watchdog
- requests
- Pillow






# Executive Summary

## Project Outline
For our project, we have decided to create a two component application, designed to attract new users in the portfolio management space for stocks and ETFs. The CLI portion of our project is designed to be a free teaser for new users. The streamlit portion of our project is designed to be subscription based, for users who enjoyed our CLI component and would like to further explore our applications.

## The Core
The core of our project is essentially a portfolio analyzer that analyzes the returns of three different sectors of stocks/ETFs (Tech, Real Estate, Energy) across three different time periods (pre-pandemic, pandemic, post-pandemic), in order to analyze which sector(s) would have been the best to invest in for each time period(s). Of the three sectors chosen, six assets were chosen to track. The six assets include sector leading individual stocks, and sector wide broad based ETFs. Also, selected was a proxy ETF for the S&P 500 as a benchmark. 

### Stocks & ETFs
- `AMZN` - Amazon.com, Inc.
- `AMT` - American Tower Corp
- `XOM` - Exxon Mobil Corp
- `XLE` - Energy Select Sector SPDR ETF Fund
- `IYR` - iShares US Real Estate ETF
- `RTH` - VanEck Retail ETF
- `SPY` - S&P500 ETF

### Time Periods
#### Pre-pandemic:
- start_date = 2017-03-01
- end_date = 2020-03-01

#### Pandemic:
- start_date = 2020-03-01
- end_date = 2022-03-01

#### Post-pandemic:
- start_date = 2022-03-01
- end_date = 2022-011-01


### Analysis
To analyze each sector and time period, we used a variety of metrics and statistics, such as Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio.


### Results

#### Pre-Pandemic Results:
As expected most of the sectors were experiencing a growth environment. This was consistent with the rest of the economy at large. We found the Technology sector to be the best performing sector, as a whole as the Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio were highest in this sector. It is important to note, in particular, investing in AMT (American Towers) would have yielded the biggest returns for the pre-pandemic period as it had the absolute highest ratios. We found the worst performing sector to be the Energy sector, with negative values for the aforementioned ratios.

#### Pandemic Results:
With a large portion of Americans at home and the ease of online shopping, the Consumer Goods sector was the first to recover from the initial shock of the economic slowdown caused by the Pandemic. We found the Technology sector to be the best performing sector, as the Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio were highest in this sector. We found the worst performing sector to be the Real Estate sector, with the lowest values for the aforementioned ratios.

#### Post-Pandemic Results:
We found the Energy sector to be the best perfoming sector, as the Sharpe Ratio, Calmar Ratio, Omega Ratio and Sortino Ratio were by far the highest in this sector. Specifically, investing in XOM (Exxon Mobile) would have yielded the greatest returns for the post-pandemic period. We found the worst performing sector to be the Technology sector, with the largest negative values for the aforementioned ratios.









