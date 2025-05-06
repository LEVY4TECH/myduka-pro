from flask import Flask,render_template,request,redirect,url_for

from database import fetch_products,fetch_sales,insert_products,insert_sales,profit_per_product,profit_per_day,sales_per_product,sales_per_day

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
    profit_p_product= profit_per_product()
    sales_p_product=sales_per_product()


    profit_p_day=profit_per_day()
    
    sales_p_day=sales_per_day()

    # list comprehension
    product_name=[i[0] for i in profit_p_product]
    p_profit=[ float(i[1]) for i in profit_p_product]
    p_sales=[ float(i[1]) for i in sales_p_product]

    # day metrics data
    date=[ str(i[0]) for i in profit_p_day]
    p_day=[ float(i[1]) for i in profit_p_day]
    s_day=[ float(i[1]) for i in sales_p_day]

    return render_template('dashboard.html',product_name=product_name,p_profit=p_profit,p_sales=p_sales,date=date,p_day=p_day,s_day=s_day)

    # return render_template('dashboard.html',profit_p_product=profit_p_product,profit_p_day=profit_p_day,sales_p_product=sales_p_product,sales_p_day=sales_p_day)

app.run(debug=True)