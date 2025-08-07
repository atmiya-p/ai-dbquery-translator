import streamlit as st
import pandas as pd
from utils.db_utils import connect_db, execute_query
from nlp.parser import parse_nl

st.title("Welcome to The SQL Query Genie")
st.markdown("Talk to your data. We got the SQL stuff from here :)")


