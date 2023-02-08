from scrapper import get_df
import streamlit as st 
from datetime import datetime

st.title("Tender History")
st.write('Source: https://msmart.mcmc.gov.my/')
df = get_df('tenderquoted')

now = datetime.now()
with open(f'tender_history_{now}.csv') as f:
    st.download_button('Download CSV', f)

st.table(df)