import streamlit as st
import pandas as pd
from utils.db_utils import connect_db, execute_query
from nlp.parser import parse_nl, get_product_list, add_products, remove_products

st.title("Welcome to The SQL Query Genie")
st.markdown("Talk to your data. We got the SQL stuff from here :)")

action = st.selectbox("What would you like to do?", ["Search Data", "Add Data", "Remove Data", "Manage Products"])

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
        product_name_input = st.selectbox("Select Product", get_product_list())
        amount_input = st.number_input("Enter amount (without $ sign and 2 decimal places)", min_value=0.00, format="%.2f")
        order_date_input = st.text_input("Enter order date (Format: YYYY-MM-DD)")

        add_button = st.button("Add Record")
        if add_button:
            if not customer_name_input or not product_name_input:
                st.error("Please make sure you have filled the customer name and product name.")
            else:
                try:
                    cursor = conn.cursor()
                    sql_query_add = f"INSERT INTO orders (customer_name, product_name, amount, order_date) VALUES ('{customer_name_input}', '{product_name_input}', {amount_input}, '{order_date_input}')"
                    cursor.execute(sql_query_add)
                    conn.commit()
                    st.success("This record was added successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    elif action == "Remove Data":
        st.markdown("Still working on this")

    elif action == "Manage Products":
        st.subheader("Manage the Products")
        product_action = st.selectbox("What would you like to do?", ["View Products", "Add Products", "Remove Products"])

        if product_action == "View Products":
            product_list = get_product_list()
            df = pd.DataFrame(product_list, columns=["Product"])
            st.dataframe(df, use_container_width=True)

        elif product_action == "Add Products":
            st.subheader("Add a new Product")
            new_product = st.text_input("Enter Name of New Product")
            add_product_button = st.button("Add Product")

            if add_product_button:
                if add_products(new_product):
                    st.success("Product was successfully added")
                else:
                    st.error("Product already exists")

        elif product_action == "Remove Products":
            st.subheader("Remove a Product")
            product_to_remove = st.selectbox("Remove Product", get_product_list())
            remove_button = st.button("Remove Product")
            if remove_button:
                if remove_products(product_to_remove):
                    st.success("Product was successfully removed")
                else:
                    st.error("Product could not be removed")

