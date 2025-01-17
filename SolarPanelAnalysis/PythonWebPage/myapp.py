import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
    # Simple Stock Price App

    Show are the stocs **closing point** and ***volume*** of the Google!

""")

tickerSymbol = 'GOOGL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2024-10-24')

st.write("""
    ## closing the plot
""")

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
