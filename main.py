import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Google Play Store App Analyse",layout="wide")



#STYLE PART
st.markdown("""<style>
            .header {
                visibility:hidden;
            }
            
            
            </style>
            """,unsafe_allow_html=True)

st.markdown("<h1> GOOGLE PLAY STORE APPLICATON ANALYSE</h1>",unsafe_allow_html=True)



# 