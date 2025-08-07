import spacy
from datetime import datetime
import sqlite3

DB_FILE_PATH = 'db/orders.db'

# using pre trained english language model - en_core_web_sm
nlp = spacy.load("en_core_web_sm")


# method to get the products in the database
def get_product_list(file_path):

    # default products we already have
    products = ["macbook", "ipad", "iphone", "apple tv", "airpods"]
    try:
        connection = sqlite3.connect(file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT LOWER(product_name) FROM orders")
        for row in cursor.fetchall():
            if row[0] not in products:
                products.append(row[0])
        connection.close()
    except Exception as exception:
        print("There was an issue with fetching the product names from the db: ", exception)
    return products


def parse_nl(query):
    doc_object = nlp(query.lower())

    entities = {"date": None, "person": None, "product": None}

    # https://spacy.io/api/entityrecognizer
    for entity in doc_object.ents:
        if entity.label_ == "DATE":
            entities["date"] = entity.text
        elif entity.label_ == "PERSON":
            entities["person"] = entity.text

    products = get_product_list(DB_FILE_PATH)
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
                conditions_list.append(f"order_date = '{date_in_format}'")
            except ValueError:
                try:
                    date_object = datetime.strptime(date_string, "%Y")
                    date_in_format = date_object.strftime('%Y')
                    conditions_list.append(f"order_date = '{date_in_format}'")
                except ValueError:
                    conditions_list.append(f"order_date LIKE '%{date_string}%")

    if entities["person"]:
        person = entities["person"].title()
        conditions_list.append(f"customer_name = '{person}'")

    if entities["product"]:
        product = entities["product"].lower()
        conditions_list.append(f"product_name = '{product}'")

    if conditions_list:
        new_query = f"'{select_all_query}' WHERE " + " AND ".join(conditions_list)
    else:
        new_query = select_all_query

    return new_query
