from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie


# Set page configurations - ALWAYS at the top
st.set_page_config(page_title="COVID portfolio analyzer", page_icon=":bar_chart:",layout="wide")

# Create a function to access the json data of the Lottie animation using requests - if successful return 200 - data is good, show animation else return none
def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

# Use local style.css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
        
local_css("style/style.css")        
    
# Load assets 
lottiefiles_gif=load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_ghysqmiq.json")
img_amt_pan_tearsheet=Image.open("./Images/amt_pan_tearsheet.png")
img_amzn_pan_tearsheet=Image.open("./Images/amzn_pan_tearsheet.png")
img_iyr_pan_tearsheet=Image.open("./Images/iyr_pan_tearsheet.png")
img_rth_pan_tearsheet=Image.open("./Images/rth_pan_tearsheet.png")
img_xle_pan_tearsheet=Image.open("./Images/xle_pan_tearsheet.png")
img_xom_pan_tearsheet=Image.open("./Images/xom_pan_tearsheet.png")
img_spy_pan_tearsheet=Image.open("./Images/spy_pan_tearsheet.png")

"""
## Welcome to the COVID financial portfolio analyzer

The web app analyzes stocks & ETFs against the S&P500 index using [polygon.io](https://polygon.io/stocks) APIs

We used the [streamlit](https://docs.streamlit.io) python package to deploy the web app :computer:
"""

# 2 columns - title vs gif
with st.container():
     st.write("---")
     left_column,right_column=st.columns(2)
     with left_column:
          st.title("Financial analysis of stocks & ETFs against the S&P500 index")
     with right_column:
        st_lottie(lottiefiles_gif,height="75",key="finance") 
        
# Tearsheets
with st.container():
    st.write("---")
    st.header("Tearsheets - AMT, AMZN, IYR, RTH, XLE, XOM, SPY")
    image_column_1,image_column_2,image_column_3,image_column_4,image_column_5,image_column_6,image_column_7=st.columns((1,1,1,1,1,1,1))
    with image_column_1:
        st.write("American Tower Corp")
        st.image(img_amt_pan_tearsheet)
    with image_column_2:
        st.write("Amazon.com, Inc.")
        st.image(img_amzn_pan_tearsheet)
    with image_column_3:
        st.write("iShares US Real Estate ETF")
        st.image(img_iyr_pan_tearsheet)
    with image_column_4:
        st.write("VanEck Retail ETF")
        st.image(img_rth_pan_tearsheet)
    with image_column_5:
        st.write("Energy Select Sector SPDR ETF Fund")
        st.image(img_xle_pan_tearsheet)
    with image_column_6:
        st.write("Exxon Mobil Corp")
        st.image(img_xom_pan_tearsheet)
    with image_column_7:
        st.write("S&P500 ETF")
        st.image(img_spy_pan_tearsheet)
        
# Contact Form
with st.container():
    st.write("---")
    st.subheader("Message us")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/jha.ayush85@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()