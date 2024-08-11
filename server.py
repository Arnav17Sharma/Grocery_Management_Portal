from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from sql_connection import get_sql_connection
import mysql.connector
import json

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)

connection = get_sql_connection()

# NO USE OF THIS ROUTE FOR NOW
@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# DONE
@app.route('/getProducts', methods=['GET', 'POST'])
def get_products():
    if request.method == 'POST':
        product_name = request.form['prod_name']
        uom_id = request.form['uom_id']
        price_per_unit = request.form['price_per_unit']
        request_payload = {
            "product_name": product_name,
            "uom_id": uom_id,
            "price_per_unit": price_per_unit
        }
        print(request_payload)
        product_id = products_dao.insert_new_product(connection, request_payload)
        # response = jsonify({
        #     'product_id': product_id
        # })
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # return redirect(url_for('get_products'))
        # flash(f"New product added named {product_name} with uom type of {uom_id} and price/unit as {price_per_unit}")
    response = products_dao.get_all_products(connection)
    # response = jsonify(response)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response
    return render_template("manage-product.html", response=response, len = len(response))

# PENDING
@app.route('/insertProduct', methods=['GET', 'POST'])
def insert_product():
    # if request.method == 'POST':
    #     product_name = request.form['prod_name']
    #     uom_id = request.form['uom_id']
    #     price_per_unit = request.form['price_per_unit']
    #     request_payload = {
    #         "product_name": product_name,
    #         "uom_id": uom_id,
    #         "price_per_unit": price_per_unit
    #     }
    #     print(request_payload)
    #     product_id = products_dao.insert_new_product(connection, request_payload)
    #     # response = jsonify({
    #     #     'product_id': product_id
    #     # })
    #     # response.headers.add('Access-Control-Allow-Origin', '*')
    #     # return redirect(url_for('get_products'))
    #     # flash(f"New product added named {product_name} with uom type of {uom_id} and price/unit as {price_per_unit}")
    #     return render_template("new_product.html")
    # else:
    return render_template("new_product.html")

# DONE
@app.route('/getOrders', methods=['GET', 'POST'])
def get_all_orders():
    if request.method == 'POST':
        # result = request.get_json()
        # result = json.loads(result)
        # orderDetails = list(result)
        # print(type(result))
        data = request.form['data']
        result = list(eval(data))
        customer_name = request.form['customer_name']
        total = request.form['total']
        request_payload = {
            "customer_name": customer_name,
            "grand_total": total,
            "order_details": []
        }
        for i in result:
            request_payload['order_details'].append(i)
        print(request_payload)
        ordered = orders_dao.insert_order(connection, request_payload)
        print(ordered)
    response = orders_dao.get_all_orders(connection)
    # response = jsonify(response)
    # for i in response:
    #     print(i)
    # return response
    return render_template("index.html", response=response)

# PENDING
@app.route('/insertOrder', methods=['GET', 'POST'])
def insert_order():
        # print("New Order added with OrderID:", order_id)
    # request_payload = json.loads(request.form['data'])
    # order_id = orders_dao.insert_order(connection, request_payload)
    # response = jsonify({
    #     'order_id': order_id
    # })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response = products_dao.get_all_products(connection)
    # return response
    return render_template("new_order.html", response=response, len=len(response))

# PENDING
@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    if request.method == 'POST':
        prod_id = request.form['product_id']
        return_id = products_dao.delete_product(connection, prod_id)
        response = jsonify({
            'product_id': return_id
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return redirect('/getProducts')

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(debug=True)
