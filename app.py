import streamlit as st
import pandas as pd
from utils.db_utils import connect_db, execute_query
from nlp.parser import parse_nl

st.title("Welcome to The SQL Query Genie")
st.markdown("Talk to your data. We got the SQL stuff from here :)")

action = st.selectbox("What would you like to do?", ["Search Data", "Add Data", "Remove Data"])

conn = connect_db()

if isinstance(conn, str):
    st.error(conn)
else:
    if action == "Search Data":
        st.subheader("Enter your question")
        user_input = st.text_input("Query in plain english")

        if user_input:
            with st.spinner("Parsing your question"):
                sql_query = parse_nl(user_input)

                st.subheader("Generated SQL Query")
                st.code(sql_query, language="sql")


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

            '''
   order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    amount FLOAT,
    order_date DATE
        '''
    elif action == "Add Data":
        st.subheader("Add a new record")
        customer_name_input = st.text_input("Enter customer name")
        product_id_input = st.number_input("Enter product id", min_value=0, step=1)
        product_name_input = st.text_input("Enter product name")
        amount_input = st.number_input("Enter amount (without $ sign and 2 decimal places)", min_value=0.00, format="%.2f")
        order_date_input = st.text_input("Enter order date (Format: YYYY-MM-DD)")

        add_button = st.button("Add Record")
        if add_button:
            if not customer_name_input or not product_id_input or not product_name_input:
                st.error("Please make sure you have filled the customer name, product id, and product name.")
            else:
                sql_query_add = f"INSERT INTO orders (customer_name, product_id, product_name, amount, order_date) VALUES ('{customer_name_input}', {product_id_input}, '{product_name_input}', {amount_input}, '{order_date_input}')"
                result = execute_query(conn, sql_query_add)
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.success("This record was added successfully!")

    elif action == "Remove Data":
        st.markdown("Still working on this")

