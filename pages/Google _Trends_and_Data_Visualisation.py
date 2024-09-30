import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="Google Play Store App Analyse",layout="wide")

pd.options.display.float_format = '{:,.2f}'.format


#STYLE PART
st.markdown("""<style>
            .header {
                visibility:hidden;
            }
            </style>
            """,unsafe_allow_html=True)


def clear_nan(df,month):
    if df.isna().values.any():
        df.dropna(inplace=True)
    if month in df.columns:
        df[month] = pd.to_datetime(df[month])
        
    else:
        raise KeyError(f"The column '{month}' does not exist in the DataFrame.")
    
    return df
    

# Define the locators and formatter globally or pass them as arguments later
year = mdates.YearLocator()
month = mdates.MonthLocator()
year_formatter = mdates.DateFormatter("%Y")

@st.cache_resource
class TSLA:
    def __init__(self):
        # Initialize the data and perform validation
        self.df = pd.read_csv('TESLA Search Trend vs Price.csv')
        self.data_validation()
        self.price_vs_search()

    def data_validation(self):
        self.df = clear_nan(self.df,"MONTH")
    def price_vs_search(self):
        # Create the figure and axis for the plot
        self.fig =plt.figure(figsize=(14, 8), dpi=120,edgecolor="red")
        self.fig.gca().set_facecolor("black")
        self.fig.patch.set_facecolor("black")
        self.fig.set_edgecolor("red")
        self.ax1 = plt.gca()
        self.ax1.set_title("Tesla Stock Price vs Search Volume",fontsize =18,color="white")
        self.ax1.tick_params(axis='x', rotation=45)

        self.ax2 = self.ax1.twinx()
        self.ax2.tick_params(axis="y",colors = "white")
        self.ax1.set_xlim([self.df.MONTH.min(), self.df.MONTH.max()])
        self.ax1.set_ylim([0, max(self.df.TSLA_USD_CLOSE.max(), self.df.TSLA_WEB_SEARCH.max()) + 500])
        self.ax2.set_ylim([0, self.df.TSLA_WEB_SEARCH.max() + 50])
        self.ax1.tick_params(axis='x', rotation=45, colors="white")  
        self.ax1.tick_params(axis='y', colors="white")  
        

        self.ax1.set_ylabel("TSLA Stock Price", color="red")
        self.ax2.set_ylabel("TSLA Web Search Volume", color="yellow")
        
        self.ax1.xaxis.set_major_locator(year)
        self.ax1.xaxis.set_major_formatter(year_formatter)
        self.ax1.xaxis.set_minor_locator(month)
        
        self.ax1.plot(self.df.MONTH, self.df.TSLA_USD_CLOSE, color="red", label="Stock Price")
        self.ax2.plot(self.df.MONTH, self.df.TSLA_WEB_SEARCH, color="yellow", label="Web Search Volume")
        
        self.ax1.legend(loc="upper left")
        self.ax2.legend(loc="upper right")
        for spine in self.ax1.spines.values():
            spine.set_edgecolor("white")
            
        for spine in self.ax2.spines.values():
            spine.set_edgecolor("white")  

@st.cache_resource
class BTC:
    def __init__(self) :
        self.df_price = pd.read_csv('Daily Bitcoin Price.csv')
        self.df_search = pd.read_csv('Bitcoin Search Trend.csv')
        self.data_validation()
        self.df_montly = self.df_price.resample("M",on="DATE").last()

        self.price_vs_search()
    def data_validation(self):
        self.df_price = clear_nan(self.df_price,"DATE")
        self.df_search = clear_nan(self.df_search,"MONTH")
        
    def price_vs_search(self):
        self.fig =plt.figure(figsize=(14, 8), dpi=120,edgecolor="red")
        self.fig.gca().set_facecolor("black")
        self.fig.patch.set_facecolor("black")
        self.fig.set_edgecolor("red")
        self.ax1 = plt.gca()
        self.ax1.set_title("Bitcoin News Search vs Resampled Price",fontsize=18,color="white")
        self.ax1.tick_params(axis='x', rotation=45)

        self.ax2 = self.ax1.twinx()
        self.ax2.tick_params(axis="y",colors = "white")
        self.ax1.set_xlim([self.df_montly.index.min(), self.df_montly.index.max()])
        self.ax1.set_ylim([0,self.df_price.CLOSE.max() +1000])
        self.ax2.set_ylim(0,self.df_search.BTC_NEWS_SEARCH.max()+55)
        self.ax1.tick_params(axis='x', rotation=45, colors="white")  
        self.ax1.tick_params(axis='y', colors="white")  
        

        self.ax1.set_ylabel("BTC Price", color="orange")
        self.ax2.set_ylabel("Search Trend", color="skyblue")
        
        self.ax1.xaxis.set_major_locator(year)
        self.ax1.xaxis.set_major_formatter(year_formatter)
        self.ax1.xaxis.set_minor_locator(month)
        
        self.ax1.plot(self.df_montly.index,self.df_montly.CLOSE, color="orange",linewidth=3, linestyle='--', label = " BTC Price")
        self.ax2.plot(self.df_montly.index, self.df_search.BTC_NEWS_SEARCH, color='skyblue', linewidth=3, marker='o',label= "Search Trend" )
        
        self.ax1.legend(loc="upper left")
        self.ax2.legend(loc="upper right")
        for spine in self.ax1.spines.values():
            spine.set_edgecolor("white")
            
        for spine in self.ax2.spines.values():
            spine.set_edgecolor("white")  




@st.cache_resource
class Unemployment:
    def __init__(self):
        self.df_19 = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')
        self.df_20 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')
        self.data_validation()
    def data_validation(self):
        self.df_19 = clear_nan(self.df_19,"MONTH")
        self.df_20 = clear_nan(self.df_20,"MONTH")
        
    
    def plot_graph(self,df):
        self.df = df
        roll_df = self.df[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=3).mean()
        self.fig = plt.figure(figsize=(14,8),dpi=120)
        self.fig.gca().set_facecolor("black")
        self.fig.patch.set_facecolor("black")
        
        self.ax1 = plt.gca()
        self.ax1.grid(False)
        self.ax1.set_title("Monthly Search of 'Unemployment Benefits' in the U.S. vs the U/E Rate",fontsize =18,color="white")
        
        self.ax2 = self.ax1.twinx()
        self.ax2.grid(False)

        self.ax1.set_xlim([self.df.MONTH.min(), self.df.MONTH.max()])
        self.ax1.set_ylim(0,roll_df.UE_BENEFITS_WEB_SEARCH.max())
        self.ax2.set_ylim(0,roll_df.UNRATE.max() +150)
        self.ax1.tick_params(axis='x', rotation=45, colors="white")  
        self.ax1.tick_params(axis='y', colors="white")  
        self.ax2.tick_params(axis="y",colors = "white")
        
        self.ax1.set_ylabel("FRED U/E Rate", color="orange")
        self.ax2.set_ylabel("Search Trend", color="skyblue")
        
        self.ax1.xaxis.set_major_locator(year)
        self.ax1.xaxis.set_major_formatter(year_formatter)
        self.ax1.xaxis.set_minor_locator(month)
        
        self.ax1.plot(self.df.MONTH,roll_df.UNRATE, color="orange",linewidth=3, linestyle='--', label = " FRED U/E Rate")
        self.ax2.plot(self.df.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH, color='skyblue', linewidth=3, marker='o',label= "Search Trend" )
        
        self.ax1.legend(loc="upper left",facecolor="white")
        self.ax2.legend(loc="upper right",facecolor="white")
        for spine in self.ax1.spines.values():
            spine.set_edgecolor("white")
            
        for spine in self.ax2.spines.values():
            spine.set_edgecolor("white")  
        



tesla = TSLA()
btc = BTC()
unemp = Unemployment()
col1, col2= st.columns(2)



try :
    df_tesla = tesla.df
    df_tesla.MONTH = df_tesla.MONTH.dt.date

    df_btc_price = btc.df_price
    df_btc_price.DATE = df_btc_price.DATE.dt.date

    df_btc_search = btc.df_search
    df_btc_search.MONTH = df_btc_search.MONTH.dt.date

    df_unp19 = unemp.df_19
    df_unp19.MONTH = df_unp19.MONTH.dt.date


    df_unp20 = unemp.df_20
    df_unp20.MONTH = df_unp20.MONTH.dt.date
except:
    pass
# scnd_tab1,scnd_tab2,scnd_tab3,scnd_tab4,scnd_tab5 = st.tabs(["TESLA Stock Price vs Search Trend ", "BTC Price vs BTC Search","BTC Price vs BTC Search", "Unemployment Benefits 2019", "Unemployment Benefits 2020"])

# with col1:
#     with scnd_tab1:
#         st.pyplot(tesla.fig, use_container_width=True)
#     with scnd_tab2:
#         st.pyplot(btc.fig, use_container_width=True)
#     with scnd_tab3:
#         st.pyplot(btc.fig, use_container_width=True)

#     with scnd_tab4:
#         unemp.plot_graph(unemp.df_19)
#         st.pyplot(unemp.fig, use_container_width=True)
#     with scnd_tab5:
#         unemp.plot_graph(unemp.df_20)
#         st.pyplot(unemp.fig, use_container_width=True)

# tab1,tab2,tab3,tab4,tab5 = st.tabs(["TESLA Stock Price vs Search Trend ", "BTC Price","BTC Search", "Unemployment Benefits 2019", "Unemployment Benefits 2020"])


# with col2:
#     with tab1:
#         st.dataframe(tesla.df,use_container_width=True)
#     with tab2:
#         st.dataframe(btc.df_price,use_container_width=True)
#     with tab3:
#         st.dataframe(btc.df_search,use_container_width=True)
#     with tab4:
#         st.dataframe(unemp.df_19,use_container_width=True)

#     with tab5:
#         st.dataframe(unemp.df_20,use_container_width=True)




tab1, tab2, tab3, tab4, tab5 = st.tabs(["Tesla", "BTC Price", "BTC Search", "Unemp 2019", "Unemp 2020"])

# Tesla Tab
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(tesla.df, use_container_width=True)
    with col2:
        st.pyplot(tesla.fig, use_container_width=True)

# BTC Price Tab
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(btc.df_price, use_container_width=True)
    with col2:
        st.pyplot(btc.fig, use_container_width=True)

# BTC Search Tab
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(btc.df_search, use_container_width=True)
    with col2:
        st.pyplot(btc.fig, use_container_width=True)

# Unemp 2019 Tab
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(unemp.df_19.reset_index(drop=True,inplace=False), use_container_width=True)
    with col2:
        unemp.plot_graph(unemp.df_19)
        st.pyplot(unemp.fig, use_container_width=True)

# Unemp 2020 Tab
with tab5:
    col1, col2 = st.columns(2,gap="medium")
    with col1:
        st.dataframe(unemp.df_20, use_container_width=True)
    with col2:
        unemp.plot_graph(unemp.df_20)
        st.pyplot(unemp.fig, use_container_width=True)
