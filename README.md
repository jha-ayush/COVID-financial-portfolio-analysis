# Financial Portfolio Analysis
> [Portfolio Analyzer pitch](https://share.synthesia.io/606a3c1a-5dc5-4f5e-b62c-714122d22ebd "Avatar pitch")


> [Project presentation](https://docs.google.com/presentation/d/1h6WeGVXbMMQkdrFOkK9d-qfRLPB0UTQduO6VTPxZbtA/edit?usp=sharing "Portfolio Analyzer")

We built a portfolio analyzer tear sheet to view financial market behaviors of specific investment stocks & ETFs from FY 2017-2022 to assess the impacts of pre-COVID and post-COVID timelines. We are going to compare the data against the S&P500 index.

Tickers used for portfolio analysis:
- `AMZN` - Amazon.com, Inc.
- `AMT` - American Tower Corp
- `XOM` - Exxon Mobil Corp
- `XLE` - Energy Select Sector SPDR ETF Fund
- `IYR` - iShares US Real Estate ETF
- `RTH` - VanEck Retail ETF
- `SPY` - S&P500 ETF used for benchmarking

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
- MCForecastTools
- streamlit
- streamlit-lottie
- watchdog
- requests
- Pillow







