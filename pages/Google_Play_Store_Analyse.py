import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
st.set_page_config(page_title="Google Play Store App Analyse",layout="wide")

pd.options.display.float_format = '{:,.2f}'.format



#STYLE PART
st.markdown("""<style>
            .header {
                visibility:hidden;
            }
            
            
            </style>
            """,unsafe_allow_html=True)


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
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgb(0, 0, 0)',    
    )
    return fig
#Analyse category distrubtion
@st.cache_data
def category(df_clean):
    df_clean.Category.nunique()
    top_categories= df_clean.Category.value_counts()    
    bar = px.bar(x=top_categories.index,y=top_categories.values,color_continuous_scale="Agsunset")    
    
    return bar
def custom_tick_format(x):
    """
    Format x-axis ticks to display values in billions (B).
    """
    if x >= 1e9:
        return '{:.0f}B'.format(x * 1e-9)
    elif x >= 1e6:
        return '{:.0f}M'.format(x * 1e-6)
    elif x >= 1e3:
        return '{:.0f}K'.format(x * 1e-3)
    else:
        return '{:.0f}'.format(x)

@st.cache_data
def categories_with_highes_dowdloand(df_clean):
    # Convert 'Installs' column to numeric
    df_clean['Installs'] = pd.to_numeric(df_clean['Installs'].str.replace('[^\d.]', ''), errors='coerce')
    
    top_categories_with_highes_dowload = df_clean.groupby("Category").agg({"Installs":pd.Series.sum})
    top_categories_with_highes_dowload.sort_values("Installs",ascending=False,inplace=True)
    
    horizontal_bar = px.bar(x=top_categories_with_highes_dowload.Installs,
                            y=top_categories_with_highes_dowload.index,
                            orientation="h")

    horizontal_bar.update_layout(xaxis_title ="Number of Dowloads",
                                yaxis_title="Category",
                                 xaxis_tickformat='.0f',
                                 xaxis_tickvals=np.arange(0, top_categories_with_highes_dowload.Installs.max(), step=1e9),  # Adjust tick values as needed
                                 xaxis_ticktext=[custom_tick_format(x) for x in np.arange(0, top_categories_with_highes_dowload.Installs.max(), step=1e9)])  # Apply custom tick format

    return horizontal_bar

    
    

@st.cache_data    
def genres_graph(df_clean):
    genres = df_clean.Genres.str.split(";",expand=True).stack()
    num_genres = genres.value_counts()
    color_bar= px.bar(x=num_genres.index,
                    y=num_genres.values,
                    color=num_genres.values,
                    hover_name=num_genres.index,
                    color_continuous_scale="Agsunset")

    color_bar.update_layout(xaxis_title="Genre",
                    yaxis_title ="Number of Aoos",
                    coloraxis_showscale=True
                    )
    return color_bar




@st.cache_data    
def free_vs_paid(df_clean):
    df_free_vs_paid = df_clean.groupby(["Category","Type"],as_index=False).agg({"App":pd.Series.count})
    df_free_vs_paid.sort_values("App",ascending=False)
    g_bar = px.bar(df_free_vs_paid,
                x="Category",
                y="App",
                color="Type",
                title="Free vs Paid Apps by Category",
                barmode="group")

    g_bar.update_layout(xaxis_title='Category',
                        yaxis_title='Number of Apps',
                        xaxis={'categoryorder':'total descending', "tickmode":'array' },
                                 yaxis={'type': 'log',
                                        'tickvals': [1, 10, 100, 1000],
                                        'ticktext': ['1', '10', '100', '1000']})
    
    return g_bar


@st.cache_data    
def box_plot_paid_apps(df_clean):
    box_plot = px.box(df_clean,
                    y="Installs",
                    x="Type",
                    color="Type",
                    notched=True,
                    points="all",
                    title= "Me")

    box_plot.update_layout(                                 yaxis={'type': 'log',
                                        'tickvals': [1, 10, 100, 1000],
                                        'ticktext': ['1', '10', '100', '1000']}
)
    return box_plot



@st.cache_data
def revenue_by_category(df_clean):
    df_paid_apps = df_clean[df_clean['Type'] == 'Paid']
    box = px.box(df_paid_apps,
                x='Category',
                y='Price',
                title='How Much Can Paid Apps Earn?')

    box.update_layout(xaxis_title='Category',
                    yaxis_title='Paid App Price',
                    xaxis={'categoryorder':'max descending'},
                    yaxis=dict(type='log'))

    return box    


st.markdown("<h1> GOOGLE PLAY STORE APPLICATON ANALYSE</h1>",unsafe_allow_html=True)


df_highest_rating = highest_rated_apps(df_clean)
df_highest_size = highest_size_apps(df_clean)
df_highest_reviews = highest_reviews_apps(df_clean)
df_highest_revenue = highest_revenue(df_clean)
df_app_installs = highest_installs(df_clean)
plot_content_rating = content_rating(df_clean)
plot_install_distrubtion = install_distrubition(df_clean)
plot_category_dist = category(df_clean)
plot_categories_with_highes_down = categories_with_highes_dowdloand(df_clean)
plot_genres_graph = genres_graph(df_clean)
plot_freeVs_paid = free_vs_paid(df_clean)
plot_box_plot_paid_apps = box_plot_paid_apps(df_clean)
plot_revenue_by_category = revenue_by_category(df_clean)



tab1,tab2,tab3,tab4,tab5 = st.tabs(["Highest Rated","Highest Size(MBs)","Highest Reviews","Highest Revenue","Installs"])
with tab1:
    st.dataframe(df_highest_rating,use_container_width=True)
with tab2:
    st.dataframe(df_highest_size,use_container_width=True)
with tab3:
    st.dataframe(df_highest_reviews,use_container_width=True)
with tab4:
    st.dataframe(df_highest_revenue,use_container_width=True)
    
with tab5:
    st.dataframe(df_app_installs,use_container_width=True)
        




col_tab1,col_tab2,col_tab3,col_tab4,col_tab5,col_tab6,col_tab7,col_tab8 = st.tabs(["Content Rating Distribution","Install Distribution","Category Distribution","Categories with Dowloand","Genre Distribution","Free vs Paid App Comparison","Box Plot: Paid vs Free","Revenue by Category"])   

with col_tab1:
    st.plotly_chart(plot_content_rating,use_container_width=True)
with col_tab2:
    st.plotly_chart(plot_install_distrubtion,use_container_width=True)
with col_tab3:
    st.plotly_chart(plot_category_dist,use_container_width=True)
with col_tab4:
    st.plotly_chart(plot_categories_with_highes_down,use_container_width=True)
with col_tab5:
    st.plotly_chart(plot_genres_graph,use_container_width=True)
with col_tab6:
    st.plotly_chart(plot_freeVs_paid,use_container_width=True)
with col_tab7:
    st.plotly_chart(plot_box_plot_paid_apps,use_container_width=True)
with col_tab8:
    st.plotly_chart(plot_revenue_by_category,use_container_width=True)
