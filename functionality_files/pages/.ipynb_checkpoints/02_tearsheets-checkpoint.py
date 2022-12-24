# Display *pyfolio* tearsheets

# Import libraries
from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# Set page configurations - ALWAYS at the top
st.set_page_config(page_title="COVID portfolio analyzer",page_icon=":bar_chart:",layout="centered")


# Use local style.css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
        
local_css("./style/style.css")        

# Load assets 
img_amt_pan_tearsheet=Image.open("../Images/AMT.png")
img_amzn_pan_tearsheet=Image.open("../Images/AMZN.png")
img_iyr_pan_tearsheet=Image.open("../Images/IYR.png")
img_rth_pan_tearsheet=Image.open("../Images/RTH.png")
img_xle_pan_tearsheet=Image.open("../Images/XLE.png")
img_xom_pan_tearsheet=Image.open("../Images/XOM.png")
img_spy_pan_tearsheet=Image.open("../Images/SPY.png")

# Create a dictionary for the tickers
imgs_dict={"AMT":img_amt_pan_tearsheet,"AMZN":img_amzn_pan_tearsheet,"IYR":img_iyr_pan_tearsheet,"RTH":img_rth_pan_tearsheet,"XLE":img_xle_pan_tearsheet,"XOM":img_xom_pan_tearsheet,"SPY":img_spy_pan_tearsheet}

# Add Title
st.title(f"Tearsheets")
# Create a selectbox
img_dict=st.selectbox("Which ticker tearsheet would you like to view?",imgs_dict)

# Display specific ticker for each symbol
if img_dict == "AMT":
    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    image = Image.open("../Images/AMT.png")
    st.image(image, caption='AMT Tearsheet', width=width)
elif img_dict == "AMZN":
    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    image = Image.open("../Images/AMZN.png")
    st.image(image, caption='AMZN Tearsheet', width=width)
elif img_dict == "IYR":
    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    image = Image.open("../Images/IYR.png")
    st.image(image, caption='IYR Tearsheet', width=width)
elif img_dict == "RTH":
    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    image = Image.open("../Images/RTH.png")
    st.image(image, caption='RTH Tearsheet', width=width)
elif img_dict == "XLE":
    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    image = Image.open("../Images/XLE.png")
    st.image(image, caption='XLE Tearsheet', width=width)
elif img_dict == "XOM":
    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    image = Image.open("../Images/XOM.png")
    st.image(image, caption='XOM Tearsheet', width=width)
else:
    width = st.slider('What width would you like in pixels?', 0, 700, 350)
    image = Image.open("../Images/SPY.png")
    st.image(image, caption='SPY Tearsheet', width=width)
# st.snow()
st.balloons()
    


