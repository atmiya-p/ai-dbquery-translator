import streamlit as st
import pandas as pd
from utils.db_utils import connect_db, execute_query
from nlp.parser import parse_nl

st.title("Welcome to The SQL Query Genie")
st.markdown("Talk to your data. We got the SQL stuff from here :)")

st.subheader("Enter your question")
user_input = st.text_input("Query in plain english")

if user_input:
    with st.spinner("Parsing your question"):
        sql_query = parse_nl(user_input)

    st.subheader("Generated SQL Query")
    st.code(sql_query, language="sql")

    conn = connect_db()

    if isinstance(conn, str):
        st.error(conn)
    else:
        with st.spinner("Executing query"):
            result = execute_query(conn, sql_query)

        if isinstance(result, str):
            st.error(result)
        else:
            columns, rows = result
            if rows:
                st.success(f"Found {len(rows)} rows")
                df = pd.DataFrame(rows, columns=columns)
                st.dataframe(df, use_container_width=True)

            else:
                st.warning("No results for that query")
