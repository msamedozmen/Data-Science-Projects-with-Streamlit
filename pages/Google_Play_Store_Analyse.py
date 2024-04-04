import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="Google Play Store App Analyse",layout="wide")

pd.options.display.float_format = '{:,.2f}'.format


@st.cache_data

def read_csv():
    df = pd.read_csv('apps.csv')
    return df


df = read_csv()

#Data Cleaning 

@st.cache_data
def data_cleaning(df):
    df_clean = df.dropna()
    df_clean = df_clean.drop_duplicates(subset=["App","Price","Type"])
    return df_clean
    

#Highest Rated Apps
@st.cache_data
def highest_rated_apps(df_clean):
    df_highest_rating = df_clean.sort_values("Rating",ascending=False,ignore_index=True,)
    return df_highest_rating

#Highest Size Apps
@st.cache_data
def highest_size_apps(df_clean):
    return df_clean.sort_values("Size_MBs",ascending=False,ignore_index=True)

@st.cache_data   
def highest_reviews_apps(df_clean):
    return df_clean.sort_values("Reviews",ascending=False,ignore_index=True)


def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df


@st.cache_data
def highest_revenue (df_clean):
    df_clean.Installs = pd.to_numeric(df_clean.Installs.astype(str).str.replace(",",""))
    df_clean.Price = pd.to_numeric(df_clean.Price.astype(str).str.replace("$","",regex=False))
    df_clean["Revenue"]= df_clean.Installs.mul(df_clean.Price)
    temp_cols=df_clean.columns.tolist()
    used_column = ['App', 'Category', 'Revenue']
    columns_ordered = ['App', 'Category', 'Revenue'] + [ name for name in temp_cols if name not in used_column]
    df_clean = df_clean[columns_ordered]

    return df_clean.sort_values(by="Revenue",ascending=False)

df_clean = data_cleaning(df)




#STYLE PART
st.markdown("""<style>
            .header {
                visibility:hidden;
            }
            
            
            </style>
            """,unsafe_allow_html=True)

st.markdown("<h1> GOOGLE PLAY STORE APPLICATON ANALYSE</h1>",unsafe_allow_html=True)


df_highest_rating = highest_rated_apps(df_clean)
df_highest_size = highest_size_apps(df_clean)
df_highest_reviews = highest_reviews_apps(df_clean)
df_highest_revenue = highest_revenue(df_clean)

col1,col2 = st.columns([0.6,0.45])


with col1:
    tab1,tab2,tab3,tab4 = st.tabs(["Highest Rated","Highest Size(MBs)","Highest Reviews","Highest Revenue"])
    with tab1:
        st.dataframe(df_highest_rating)
    with tab2:
        st.dataframe(df_highest_size)
    with tab3:
        st.dataframe(df_highest_reviews)
    with tab4:
        st.dataframe(df_highest_revenue)