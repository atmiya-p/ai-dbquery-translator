import spacy
from datetime import datetime
import sqlite3

DB_FILE_PATH = 'db/orders.db'

# using pre trained english language model - en_core_web_lg
nlp = spacy.load("en_core_web_lg")

products = []


# method to get the products in the database
def get_product_list():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT product_name FROM products ORDER BY product_name")
    all_products = cursor.fetchall()
    conn.close()
    list_of_all_products = []
    for product in all_products:
        product_name = product[0]
        list_of_all_products.append(product_name)
    return list_of_all_products


def add_products(product):
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (product_name) VALUES (?)", (product.lower(),))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False


def remove_products(product):
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_name = ?", (product.lower(),))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False


def parse_nl(query):
    doc_object = nlp(query.lower())

    entities = {"date": None, "person": None, "product": None}

    # https://spacy.io/api/entityrecognizer
    for entity in doc_object.ents:
        if entity.label_ == "DATE":
            entities["date"] = entity.text
        elif entity.label_ == "PERSON":
            entities["person"] = entity.text

    products = get_product_list()
    for token in doc_object:
        if token.text in products:
            entities["product"] = token.text
            break

    select_all_query = "SELECT * FROM orders"
    conditions_list = []  # will store all conditions in here and append later to the select all query

    if entities["date"]:
        # https://www.programiz.com/python-programming/datetime/strptime
        date_string = entities["date"]
        try:
            date_object = datetime.strptime(date_string, "%B %d, %Y")
            date_in_format = date_object.strftime('%Y-%m-%d')
            conditions_list.append(f"order_date = '{date_in_format}'")
        except ValueError:
            try:
                date_object = datetime.strptime(date_string, "%B %Y")
                date_in_format = date_object.strftime('%Y-%m')
                conditions_list.append(f"order_date LIKE '{date_in_format}%'")
            except ValueError:
                try:
                    date_object = datetime.strptime(date_string, "%Y")
                    date_in_format = date_object.strftime('%Y')
                    conditions_list.append(f"order_date LIKE '{date_in_format}%'")
                except ValueError:
                    conditions_list.append(f"order_date LIKE '%{date_string}%'")

    if entities["person"]:
        person = entities["person"].lower()
        conditions_list.append(f"LOWER(customer_name) = '{person}'")

    if entities["product"]:
        product = entities["product"].lower()
        conditions_list.append(f"LOWER(product_name) = '{product}'")

    if conditions_list:
        new_query = f"{select_all_query} WHERE " + " AND ".join(conditions_list)
    else:
        new_query = select_all_query

    return new_query
