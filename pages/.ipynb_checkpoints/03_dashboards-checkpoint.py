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
        
local_css("style/style.css")
        

# Visualizations
with st.container():
    st.header("Dashboards")
    st.write("---")