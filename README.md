# SQL Query Genie
**A natural language to SQL translator with Streamlit-UI, backed by an SQLite database.**

Users can ask plain English questions such as *Show me all orders from John Smith in July 2025*, and the web app will parse the query into SQL, fetch the results, and display them. It will also display the query it generated, allowing the user to learn more if they wish.

Users are able to **add and remove records to the database** in a user-friendly way, and the app does all the back-end database work.

## Features
* ### Natural Language Processing (NLP)
  * Converts plain English queries into valid SQL using spaCy
  * Recognises dates, names, and products
* ### Order Management
  * Adds new records with customer, product, amount and order date
  * Search orders with natural language queries
* ### Product Management
  * Can add, view, and remove products in the database
  * When adding new orders, products are selectable
* ### Steamlit UI
  *   Very user-friendly interface. Created keeping UX principles in mind

## Tech Stack
* Frontend: *Streamlit*
* NLP: *spaCy*
* Database: *SQLite3*
* Language *Python3*

# Example Queries
* English --> SQL Translation

  ```
  User Input: "Show me all orders from John Smith in July 2025"
  Output: SELECT * FROM orders WHERE LOWER(customer_name) = 'john smith' AND order_date LIKE '2025-07%'
  ```
