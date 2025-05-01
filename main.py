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
        productName=request.form['']
        buying_price=request.form['']
        selling_price=request.form['']
        stock_quantity=request.form['']
        new_product=(productName,buying_price,selling_price,stock_quantity)
        insert_products(new_product)
        return redirect(url_for('products'))
    
@app.route('/sales')
def sales():
    sales=fetch_sales()
    products=fetch_products
    return render_template('sales.html',sales=sales,products=products)

@app.route('/make_sale',methods=['POST'])
def make_sale():
    productsid=request.form['']
    quantity=request.form['']
    new_sale=(productsid,quantity)
    insert_sales(new_sale)
    return redirect(url_for('sales'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashborad.html')

app.run(debug=True)