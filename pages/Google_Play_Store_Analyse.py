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

@st.cache_data
def highest_installs(df_clean):
    df_clean.Installs = pd.to_numeric(df_clean.Installs.astype(str).str.replace(",",""))
    df_installs =df_clean[["App","Installs"]]
    df_installs = df_installs.sort_values(by="Installs",ascending=False)
    df_installs["Installs"] = df_installs["Installs"].apply(lambda x: "+" + str(x) if x > 10000 else str(x))
    return df_installs

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
df_app_installs = highest_installs(df_clean)

col1,col2 = st.columns([0.6,0.45])


with col1:
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Highest Rated","Highest Size(MBs)","Highest Reviews","Highest Revenue","Installs"])
    with tab1:
        st.dataframe(df_highest_rating)
    with tab2:
        st.dataframe(df_highest_size)
    with tab3:
        st.dataframe(df_highest_reviews)
    with tab4:
        st.dataframe(df_highest_revenue)
    
    with tab5:
        st.dataframe(df_app_installs)
        

#GRAPH ANALYSE
#Content Rating Distrubtion

@st.cache_data
def content_rating(df_clean):
    content_rating = df_clean.Content_Rating.value_counts()
    content_rating_df = pd.DataFrame({'Content_Rating': content_rating.index, 'Count': content_rating.values})
    fig = px.pie(
        content_rating_df,
        values='Count',
        names='Content_Rating',
        title='Content Rating Distribution',
        labels=content_rating_df.index,
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.Plasma
        
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgb(0, 0, 0)',     # Set paper (the outer background) color to dark
    )


    return fig


# Check Installs 

@st.cache_data

def install_distrubition(df_clean):
    df_clean.Installs = pd.to_numeric(df_clean.Installs.astype(str).str.replace(",",""))
    df_intalls =df_clean[["App","Installs"]].groupby("Installs").count()
    df_intalls = df_intalls.sort_values(by="App",ascending=False)
    df_intalls.index = pd.Series(df_intalls.index).apply(lambda x: "+" + str(x) if x >= 10000 else str(x))
    fig =px.pie(
        df_intalls,
        values=df_intalls.App,
        names=df_intalls.index,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgb(0, 0, 0)',     # Set paper (the outer background) color to dark
    )
    return fig
#Analyse category distrubtion
@st.cache_data
def category(df_clean):
    df_clean.Category.nunique()
    df_clean.shape
    top_categories= df_clean.Category.value_counts()    
    bar = px.bar(x=top_categories.index,y=top_categories.values,color_continuous_scale="Agsunset")    
    
with col2:
    ...
        
