from flask import Flask,render_template,request,redirect,url_for

from database import fetch_products,fetch_sales,insert_products,insert_sales

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    products=fetch_products()
    return render_template('products.html',products=products)

@app.route('/add_products',methods=['GET','POST'])
def add_products():
    if request.method=='POST':
        productName=request.form['p_name']
        buying_price=request.form['b_price']
        selling_price=request.form['s_price']
        stock_quantity=request.form['s_quantity']
        new_product=(productName,buying_price,selling_price,stock_quantity)
        insert_products(new_product)
        return redirect(url_for('products'))
    
@app.route('/sales')
def sales():
    sales=fetch_sales()
    products=fetch_products()
    return render_template('sales.html',sales=sales,products=products)

@app.route('/make_sales',methods=['POST'])
def make_sales():
    productsid=request.form['pid']
    quantity=request.form['quantity']
    new_sale=(productsid,quantity)
    insert_sales(new_sale)
    return redirect(url_for('sales'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

app.run(debug=True)