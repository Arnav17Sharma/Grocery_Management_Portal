# products_dao.py

from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    # Add a WHERE clause to only select active products
    query = """SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, products.image_url, uom.uom_name
    FROM products LEFT JOIN uom on products.uom_id = uom.uom_id
    WHERE products.is_active = 1;""" # <-- ADD THIS LINE
    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, image_url, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'image_url': image_url,
            'uom_name': uom_name
        })
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    # Add image_url to the INSERT query
    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit, image_url) "
             "VALUES (%s, %s, %s, %s)")
    # Add the image_url to the data tuple
    data = (product['product_name'], product['uom_id'], product['price_per_unit'], product['image_url'])
    cursor.execute(query, data)
    connection.commit()
    # This function doesn't need to return anything based on server.py
    # but returning lastrowid is good practice if needed.
    return cursor.lastrowid

# products_dao.py

def delete_product(connection, product_id):
    cursor = connection.cursor()
    # Change from DELETE to UPDATE to set the product as inactive
    query = "UPDATE products SET is_active = 0 WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    connection.commit()