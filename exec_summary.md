# Executive summary

### Project Outline
For our project, we have decided to create a two component application, designed to attract new users in the portfolio management space for stocks and ETFs. The CLI portion of our project is designed to be a free teaser for new users. The streamlit portion of our project is designed to be subscription based, for users who enjoyed our CLI component and would like to further explore our applications.

### The Core
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

*Pre-pandemic*:
- start_date = 2017-03-01
- end_date = 2020-03-01

*Pandemic*:
- start_date = 2020-03-01
- end_date = 2022-03-01

*Post-pandemic*:
- start_date = 2022-03-01
- end_date = 2022-11-01


### Limitations and Future Expectations
We aim to give users the best experience possible on our streamlit platform, so we have decided to include a wide variety of features that have taken more time to implement than we initially anticipated. Our streamlit platform should be available to users in the upcoming weeks. We appreciate your patience, and in the meantime, enjoy our CLI!