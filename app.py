import yfinance as yf  # type: ignore
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import joblib
from datetime import datetime

st.set_page_config("Stock Analysis Dashboard", layout="wide")
# sensex 



import yfinance as yf
from datetime import datetime

# Define index tickers
tickers = {
    "Sensex": "^BSESN",
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK",
    "Nifty IT": "^CNXIT",
    "India VIX": "^INDIAVIX"
}

display = []

# Loop through each index and fetch latest data
for name, symbol in tickers.items():
    index = yf.Ticker(symbol)
    data = index.history(period="1d")
    
    if not data.empty:
        latest_value = data['Close'].iloc[-1]
        display.append(f"{name} today ({datetime.now().date()}): {latest_value:.2f}")
    else:
        display.append(f"{name}: ❌ Data not available")

new_display = "  |  ".join(display)


# Ticker names
nse_tickers = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "State Bank of India": "SBIN.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Larsen & Toubro": "LT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "ITC": "ITC.NS",
    "Wipro": "WIPRO.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Tata Steel": "TATASTEEL.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Sun Pharmaceutical": "SUNPHARMA.NS",
    "NTPC": "NTPC.NS"
}


def fetch_stock_data(ticker , time , ticker_symbol):
    
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=time, auto_adjust=True)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].astype(str)
    data.Date = data.Date.str.split(" ").str[0]


    return data


# Side bar redesign

st.sidebar.title("Stock Analysis Dashboard")
st.sidebar.image("images.jpg", use_container_width=True)


options = ["Stock Analysis Dashboard" , "News and Curret affairs"]
selected_option  = st.sidebar.selectbox("Select the Option" , options)


if selected_option == options[0] :
    st.title("Stock Analysis Dashboard")
    st.markdown(
     f"""
     <div style="background-color:transparent; font-family: arial ;color:red; padding: 10px; border-radius: 5px; overflow: hidden; font-weight: bold;">
         <marquee behavior="scroll" direction="left" scrollamount="5" style="font-size: 25px;">
             {new_display}
         </marquee>
     </div>
     """,
     unsafe_allow_html=True
    )

    st.sidebar.header("User Input")
    ticker = st.sidebar.selectbox("Select Stock Ticker", list(nse_tickers.keys()))
    ticker_symbol = nse_tickers[ticker]


    time = st.sidebar.selectbox("Select Time Period", ["1mo" , "2mo","3mo", "6mo" , "1y", "2y", "5y", "8y" , "10y", "max"])

    # fetch_stock_data(ticker, time, ticker_symbol)
    data = fetch_stock_data(ticker, time, ticker_symbol)

    st.write("-----------------------------------------------------------------------")

    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.subheader("Date")
        st.write(data['Date'].iloc[-1])
    with col2:
        st.subheader("Today's Price")
        st.write(f"{data['Close'].iloc[-1]:.2f} INR")
    with col3:
        st.subheader("Price Change")
        change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
        change_percentage = (change / data['Close'].iloc[-2]) * 100
        st.write(f"{change:.2f} INR ({change_percentage:.2f}%)")

    col4 , col5, col6 = st.columns(3)
    with col4:
        st.subheader("Highest Price")
        st.write(f"{data['High'].iloc[-1]:.2f} INR")
    with col5:
        st.subheader("Lowest Price")
        st.write(f"{data['Low'].iloc[-1]:.2f} INR")
    with col6:
        st.subheader("Volume")
        st.write(f"{data['Volume'].iloc[-1]:.2f} INR")


    st.write("-----------------------------------------------------------------------")


    full_data  = st.sidebar.button("Show Full Data")

    if full_data:
        st.subheader(f"Full Stock Data for {ticker} for ({time})")
        st.dataframe(data)
    else:
        st.subheader(f"Stock Data for {ticker} for Last 10 days")
        st.dataframe(data.tail(10))

    st.download_button(
        label="Download Data",   
        data=data.to_csv(index=False).encode('utf-8'),
        file_name=f"{ticker}_stock_data.csv",
        mime="text/csv",
        key="download-csv"
    )


    if st.sidebar.checkbox("Show Stock information", value=True):
        ticker_info = yf.Ticker(ticker_symbol).info
        new_info = ticker_info.copy()
        st.subheader(f"Stock Information for {ticker}")
        ticker_info = {k: v for k, v in ticker_info.items() }
        ticker_info = pd.DataFrame(ticker_info.items(), columns=['Attribute', 'Value'])
        print(ticker_info)
        st.dataframe(ticker_info.head(10))
        st.download_button(
            label="Download Stock Information",
            data=ticker_info.to_csv(index=False).encode('utf-8'),
            file_name=f"{ticker}_stock_info.txt",
            mime="text/csv",
            key="download-info"
        )

    # Stock Basic Information
    st.write("-----------------------------------------------------------------------")
    col1 , col2, col3 = st.columns(3)
    with col1:
        st.subheader("Ticker Symbol")
        st.write(ticker_symbol)
    with col2:
        st.subheader("Company Name")
        st.write(ticker)
    with col3:
        st.subheader("50 Day Average")
        st.write(f"{new_info.get('fiftyDayAverage', 'N/A')} INR")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.subheader("Market Cap")
        st.write(f"{new_info.get('marketCap', 'N/A')} INR")
    with col5:
        st.subheader("52 Week Low")
        st.write(f"{new_info.get('fiftyTwoWeekLow')} INR")
    with col6:
        st.subheader("52 Week High")
        st.write(f"{new_info.get('fiftyTwoWeekHigh', 'N/A')} INR")

    st.write("-----------------------------------------------------------------------")
    # Displaying the stock data    
    st.subheader(f"Stock Closing Price for {ticker} for Last for ({time})")
    st.write("This chart shows the closing price of the selected stock over the specified time period.")
    fig = px.line(data, x='Date', y='Close', title=f"Closing Price of {ticker} for {time}")
    fig.update_layout(title_x=0.5, title_font=dict(size=20), template='plotly_white')
    fig.update_layout(xaxis_title='Date', yaxis_title='Closing Price (INR)')
    st.plotly_chart(fig, use_container_width=True)


    st.subheader(f"Stock Opening Price for {ticker} for Last for ({time})")
    # st.write("This chart shows the closing price of the selected stock over the specified time period.")
    fig = px.line(data, x='Date', y='Open', title=f"Opening Price of {ticker} for {time}")
    fig.update_layout(title_x=0.5, title_font=dict(size=20), template='plotly_white' )
    fig.update_traces(line=dict(color='green'))
    fig.update_layout(xaxis_title='Date', yaxis_title='Opening Price (INR)')
    st.plotly_chart(fig, use_container_width=True)

    # Candlestick Chart

    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])

    fig.update_layout(
        title='Stock Price Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False # Hide the range slider below the plot
    )

    st.plotly_chart(fig, use_container_width=True)


    # Moving Averages

    st.subheader(f"Moving Averages for {ticker} for Last for ({time})")
    fig = go.Figure()

    # Calculate 50-day and 200-day Simple Moving Averages (SMA)
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()


    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='gray')))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], mode='lines', name='50-Day SMA', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_200'], mode='lines', name='200-Day SMA', line=dict(color='red')))

    # Update layout
    fig.update_layout(
        title='Simulated Stock Price with 50 & 200 Day Moving Averages (Interactive)',
        xaxis_title='Date',
        yaxis_title='Price (INR)',
        legend=dict(x=0, y=1),
        hovermode='x unified',
        template='plotly_white',
        height=600,
        width=1000
    )

    st.plotly_chart(fig, use_container_width=True)


    # Yearly Analysis
    if time == "1y" or time == "2y" or time == "5y" or time == "8y" or time == "10y" or time == "max":
        st.subheader(f"Yearly Analysis for {ticker}")
        data['Year']= data.Date.str.split("-").str[0]
        data['Month'] = data.Date.str.split("-").str[1]
        yearly_data = data.groupby('Year').agg({'Open': 'mean', 'High': 'max', 'Low': 'min', 'Close': 'mean', 'Volume': 'sum', 'Dividends': 'sum', 'Stock Splits': 'sum'})
        yearly_data.reset_index(inplace=True)

        st.table(yearly_data)
        bar = px.bar(yearly_data, x='Year', y='Dividends',  template='plotly_white' , title=f"Yearly Dividends for {ticker}")
        bar.update_layout(title_x=0.5, title_font=dict(size=20), xaxis_title='Year', yaxis_title='Dividends (INR)')
        st.plotly_chart(bar , use_container_width=True)
        
        st.subheader(f"Yearly Volume Distribution for {ticker}")
        fig = px.pie(yearly_data, values = 'Volume', names = 'Year')
        fig.update_traces(textposition='outside', textinfo='percent+label')
        # fig.update_layout(title=f"Yearly Volume Distribution for {ticker}", title_x=0.5, title_font=dict(size=20), template='plotly_white')
    
        st.plotly_chart(fig, use_container_width=True)

        
        st.subheader(f"Yearly Maximun Price Distribution for {ticker}")

        st.plotly_chart(px.bar(yearly_data, x = 'Year', y = 'High' , color = 'High'))



    #monthly analysis
    if time == "1y" or time == "2y" or time == "5y" or time == "8y" or time == "10y" or time == "max":
        st.subheader(f"Monthly Analysis for {ticker}")

        year = st.selectbox("Select the Year ", data.Date.str.split("-").str[0].unique().tolist(), index=0)

        monthly_data = data.groupby(['Year' , 'Month']).agg({'Open': 'mean', 'High': 'max', 'Low': 'min', 'Close': 'mean', 'Volume': 'sum', 'Dividends': 'sum', 'Stock Splits': 'sum'})
        monthly_data.reset_index(inplace = True)
        overall_monthly_data = monthly_data.copy()
        monthly_data = monthly_data[monthly_data['Year'] == year]
        st.table(monthly_data)


        line_plot = px.line()
        line_plot.add_scatter(x=monthly_data['Month'], y=monthly_data['High'], mode='lines', name='High Price', line=dict(color='green') )
        line_plot.add_scatter(x=monthly_data['Month'], y=monthly_data['Low'], mode='lines', name='Low Price', line=dict(color='red') )
        line_plot.update_layout(title_x=0.5, title_font=dict(size=20), template='plotly_white')
        line_plot.update_layout(hovermode='x unified', height=600, width=1000 , title=f"Monthly Analysis for {ticker} in {year}")
        line_plot.update_layout(xaxis_title='Month', yaxis_title='Closing Price (INR)')
        st.plotly_chart(line_plot, use_container_width=True)


    # Monthly Volume Distribution
        st.subheader(f"Monthly Volume Distribution for {ticker} in {year}")
        monthly_volume = monthly_data.groupby('Month')['Volume'].sum().reset_index()
        fig = px.pie(monthly_volume, values='Volume', names='Month', title=f"Monthly Volume Distribution for {ticker} in {year}")
        st.plotly_chart(fig, use_container_width=True)



        Over = overall_monthly_data.groupby(['Month' , 'Year'])['Volume'].sum().reset_index().sort_values(by='Volume', ascending=False)


    # print(Over['Month'].value_counts())



    # Top 10 months with highest volume counts
    if time == "1y" or time == "2y" or time == "5y" or time == "8y" or time == "10y" or time == "max":
        st.subheader("Top 10 Months with Highest Volume Counts")
        max_volume_per_year = Over.loc[Over.groupby('Year')['Volume'].idxmax()]

        max_volume_per_year = max_volume_per_year.sort_values(by='Year')

        # Display result
        max_volume_per_year['Date'] = max_volume_per_year['Month'] + "-" + max_volume_per_year['Year']
        st.table(max_volume_per_year)

        barplot = px.bar(max_volume_per_year, x='Date', y='Volume', title=f"Monthly Volume Counts for {ticker}", template='plotly_white')
        barplot.update_layout(title_x=0.5, title_font=dict(size=20), xaxis_title='Date', yaxis_title='Volume')
        st.plotly_chart(barplot, use_container_width=True)


    #2024 Analysis

    if time == "1y" or time == "2y" or time == "5y" or time == "8y" or time == "10y" or time == "max":

        if st.sidebar.checkbox("Show 3 Year Analysis", value=True):

            st.title("3 Year Analysis for Top 3 Months with Highest Volume Counts")

            data_2024 = Over[(Over['Year'] == '2024') | (Over['Year'] == '2023') | (Over['Year'] == '2022')]
            data_3year = data_2024.sort_values(by=['Year','Volume' ], ascending=False)
            top3_per_year = data_3year.groupby('Year').head(3)
            top3_per_year['Date'] = top3_per_year['Month'] + "-" + top3_per_year['Year']
            top3_per_year.drop(columns=['Year'], inplace=True)

            st.table(top3_per_year)

            barplot_3years = px.bar(top3_per_year, x='Date', y='Volume', title=f"Top 3 Months with Highest Volume Counts", template='plotly_white')
            barplot_3years.update_layout(title_x=0.5, title_font=dict(size=20), xaxis_title='Date', yaxis_title='Volume')
            st.plotly_chart(barplot_3years, use_container_width=True)


    #key months

            key_months = data_3year.groupby('Year').head(4)
            # st.table(key_months)
            month_value = key_months['Month'].value_counts().reset_index().values.tolist()

            # month_value = [f"{month[0]}: {month[1]}" for month in month_value]

            month_value = dict(month_value)

            new_month_value = {}
            for month, value in month_value.items():
                if value >= 2:
                    new_month_value[month] = value
                else:
                    pass
                
            month_dict = {
                "January": "01",
                "February": "02",
                "March": "03",
                "April": "04",
                "May": "05",
                "June": "06",
                "July": "07",
                "August": "08",
                "September": "09",
                "October": "10",
                "November": "11",
                "December": "12"
            }

            important_months = []
            for i in new_month_value.keys():

                for key, value in month_dict.items():
                    if value == i:
                        important_months.append(key)


            # print(important_months)

            st.subheader("Important Months with Highest Volume Counts")
            st.write(pd.Series(important_months))


    if st.sidebar.checkbox("Model Prediction", value=True):
        model = joblib.load("linear_regression_model.pkl")
        st.header("Stock Price Prediction")
        st.write("This model predicts the stock price based on the historical data.")
    

        if st.button("Predict"):
            Price_yes = data['Close'].iloc[-1]  # Last 10 days of closing prices
            Price_2days_before = data['Close'].iloc[-2]
            Price_3day_before = data['Close'].iloc[-3]
            Price_4day_before = data['Close'].iloc[-4]
            Price_5day_before = data['Close'].iloc[-5]

            new = pd.DataFrame({
                'Price_yes': [Price_yes],
                'Price_2day_before': [Price_2days_before],
                'Price_3day_before': [Price_3day_before],
                'Price_4day_before': [Price_4day_before],
                'Price_5day_before': [Price_5day_before]
            })
                
            prediction = model.predict(new)
            st.subheader(f"The predicted stock price for {ticker} is: {prediction[0]:.2f} INR")


            st.write("-----------------------------------------------------------------------")
            st.write("This prediction is based on the last 5 days of closing prices.")
            st.write("Please note that stock prices are subject to market fluctuations and this prediction is for informational purposes only.")
            st.write("Always do your own research before making any investment decisions.")
            st.write("Thank you for using the Stock Analysis Dashboard!")
            st.write("-----------------------------------------------------------------------")

else:
    import feedparser
    import streamlit as st


    st.title("Market News and Current Affairs")
    st.write("This section provides the latest news and current affairs related to the stock market and economy.")
    def get_top_headlines(feed_url):
                
                feed = feedparser.parse(feed_url)
                return [entry.title for entry in feed.entries[:10]]
            
    headlines = get_top_headlines("https://www.livemint.com/rss/markets")

    news_title = ""    
    for headline in headlines:
        news_title += f"  🔴 {headline}" 
    st.markdown(
     f"""
     <div style="background-color:transparent; color:black; padding: 10px; border-radius: 5px; overflow: hidden;">
         <marquee behavior="scroll" direction="left" scrollamount="6" style="font-size: 20px;">
             {news_title }
         </marquee>
     </div>
     """,
     unsafe_allow_html=True
    )
    st.write("---" *20)
    # List of RSS feed URLs for news

    urls = [
    "https://www.moneycontrol.com/rss/markets.xml",
    "https://www.business-standard.com/rss/markets-5.rss",
    "https://www.livemint.com/rss/markets",

    ]

    for url in urls:
        print(f"Fetching news from: {url}")

        feed = feedparser.parse(url)
        flag = 0
        for entry in feed.entries:
            flag += 1
            st.subheader(f"**News {flag}: {entry.title}**")
            st.image(entry.media_content[0]['url'] if 'media_content' in entry else 'No Image')
            
            # print("Title:", entry.title)
            st.write(f"**Link:** {entry.link}")
            # print("Link:", entry.link)
            st.write (f"**Published:** {entry.published}")
            # print("Published:", entry.published)
            st.write(f"**Summary:** {entry.summary}")
            # print("Summary:", entry.summary)
            # print("Image:" , entry.get('media_thumbnail', [{'url': 'No Image'}])[0]['url'])
        

            st.write("-----" *20)

            


            

            


        










            

        
