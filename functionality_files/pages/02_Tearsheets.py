# Display *pyfolio* tearsheets

# Import libraries
from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# Set page configurations - ALWAYS at the top
st.set_page_config(page_title="COVID portfolio analyzer",page_icon=":bar_chart:",layout="wide")


# Use local style.css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
        
local_css("./style/style.css")  

ticker_list = ["AMZN", "RTH", "AMT", "IYR", "XOM", "XLE", "SPY"]
POLYGON_API_KEY = 'JQfBpF3NpcYjuBdMiXeUr6q54XafY_pQ'
    
# Load assets 
img_amt_pan_tearsheet=Image.open("../Images/AMT.png")
img_amzn_pan_tearsheet=Image.open("../Images/AMZN.png")
img_iyr_pan_tearsheet=Image.open("../Images/IYR.png")
img_rth_pan_tearsheet=Image.open("../Images/RTH.png")
img_xle_pan_tearsheet=Image.open("../Images/XLE.png")
img_xom_pan_tearsheet=Image.open("../Images/XOM.png")
img_spy_pan_tearsheet=Image.open("../Images/SPY.png")
        
# Tearsheets
with st.container():
    st.header("Tearsheets - AMT, AMZN, IYR, RTH, XLE, XOM, SPY")
    st.write("These are teaser metric snapshots of the tickers")
    st.write("---")
    st.snow()


    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    
    # iterate through the items in the array
    for ticker in ticker_list:
        # load the image file for the ticker
        image=Image.open(f"../Images/{ticker}.png")
        # display the image
        image.show()    
             

    
    # image_column_1,image_column_2,image_column_3,image_column_4,image_column_5,image_column_6,image_column_7=st.columns((1,1,1,1,1,1,1))
    # with image_column_1:
    #     st.write("American Tower Corp")
    #     st.image(img_amt_pan_tearsheet)
    # with image_column_2:
    #     st.write("Amazon.com, Inc.")
    #     st.image(img_amzn_pan_tearsheet)
    # with image_column_3:
    #     st.write("iShares US Real Estate ETF")
    #     st.image(img_iyr_pan_tearsheet)
    # with image_column_4:
    #     st.write("VanEck Retail ETF")
    #     st.image(img_rth_pan_tearsheet)
    # with image_column_5:
    #     st.write("Energy Select Sector SPDR ETF Fund")
    #     st.image(img_xle_pan_tearsheet)
    # with image_column_6:
    #     st.write("Exxon Mobil Corp")
    #     st.image(img_xom_pan_tearsheet)
    # with image_column_7:
    #     st.write("S&P500 ETF")
    #     st.image(img_spy_pan_tearsheet)