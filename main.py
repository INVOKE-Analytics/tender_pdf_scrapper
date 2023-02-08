from scrapper import get_df
import streamlit as st 

st.title("Tender History")
st.write('Source: https://msmart.mcmc.gov.my/')
df = get_df()
st.table(df)