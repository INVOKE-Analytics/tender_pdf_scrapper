from scrapper import get_df
import streamlit as st 
from datetime import datetime

st.title("Tender History")
st.write('Source: https://msmart.mcmc.gov.my/')
df = get_df('tenderquoted')

now = datetime.now()
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download CSV', csv, 'tender_history_{now}.csv', 'text/csv')

st.table(df)