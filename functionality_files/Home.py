from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie


# Set page configurations - ALWAYS at the top
st.set_page_config(page_title="COVID portfolio analyzer",page_icon=":bar_chart:",layout="wide")

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
        
local_css("./style/style.css")        
    
# Load assets 
lottiefiles_gif=load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_ghysqmiq.json")

"""
## Welcome to the COVID financial portfolio analyzer

The web app analyzes stocks & ETFs against the S&P500 index using [polygon.io](https://polygon.io/stocks) APIs

We used [streamlit](https://docs.streamlit.io) python package to deploy the web app :computer:

GIF provided via json formatting by [LottieFiles](https://lottiefiles.com/)
"""

# 2 columns - title vs gif
with st.container():
     st.write("---")
     left_column,right_column=st.columns(2)
     with left_column:
          st.title("Financial analysis of stocks & ETFs against the S&P500 index")
     with right_column:
        st_lottie(lottiefiles_gif,height="70",key="finance")
        
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

with st.container():    
    left_column, mid_column, right_column = st.columns(3)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with mid_column:
        st.empty()
    with right_column:
        st.empty()
      