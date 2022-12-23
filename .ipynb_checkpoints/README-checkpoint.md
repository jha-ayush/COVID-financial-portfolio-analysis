# COVID Portfolio Analysis

## Overview
The project aims to analyze the performance of different sectors in the stock market during and after the COVID-19 pandemic. To do this, we have developed a web application using the Python framework Streamlit, which allows us to build interactive data applications with minimal code.

The web application allows users to select a sector and a time period, and then displays the performance of that sector over the chosen period using a variety of metrics and statistics. These include the *Sharpe Ratio*, *Calmar Ratio*, *Omega Ratio*, and *Sortino Ratio*, which are commonly used to evaluate the risk-adjusted returns of investments. We calculated these ratios using the `pyfolio` python library, which provides a suite of tools for portfolio and risk analysis.

## Technology Stack
Language: Python

Web framework: Streamlit

**Libraries:** `pip install -r requirements.txt`

**API:** Polygon Stocks API

## Features
- Select a sector and a time period
- View the performance of the selected sector over the chosen period using the Sharpe Ratio, Calmar Ratio, Omega Ratio, and - Sortino Ratio
- Explore the performance of different sectors in the pre-pandemic, pandemic, and post-pandemic periods
- Running the Web Application Locally
- To run the web application locally, you will need to clone the main branch of the project from GitHub and install the required dependencies. You can do this by following these steps:

## Running the Web Application Locally
To run the web application locally, you will need to clone the main branch of the project from GitHub and install the required dependencies. You can do this by following these steps:
- `git clone` the `main` branch
- Navigate to the local directory in the terminal
- Switch to the `dev` environment using `conda activate dev`
- Install the dependencies using `pip install -r requirements.txt`
- Navigate to the `functionality_files` directory in the terminal
- Run `streamlit run Home.py` to launch the localhost app

## Data Sources
We used the Polygon Stocks API to retrieve historical financial data for different stocks and sectors. We used the requests library to make HTTP requests to the API and the pandas library to process the data and calculate the ratios. We used the Starter paywall offered by Polygon.io, which allows us to make a limited number of API calls per month.

## Team Members
Christine Pham (`cpham35`)

Kranthi Mitta (`kranthicmitta`)

Kevin Herndon (`Kevtech577`)

Ben Smookler (`BenSmook`)

Ayush Jha (`jha-ayush`)


## Links
[Presentation](https://docs.google.com/presentation/d/1h6WeGVXbMMQkdrFOkK9d-qfRLPB0UTQduO6VTPxZbtA/edit?usp=sharing)

[Web app](https://jha-ayush-finance-portfolio-analyzer-home-dnt6yf.streamlit.app/)

<sub>*Disclaimer:* The web app is currently broken online. Please access the app by running locally.</sub>