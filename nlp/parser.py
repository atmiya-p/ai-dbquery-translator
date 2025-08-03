import spacy
import datetime
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

