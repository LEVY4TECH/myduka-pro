from flask import Flask,render_template,request,redirect,url_for,flash,session

from database import fetch_products,fetch_sales,insert_products,insert_sales,profit_per_product,profit_per_day,sales_per_product,sales_per_day,check_user,insert_users,fetch_stock,insert_stock,available_stock

from flask_bcrypt import Bcrypt

from functools import wraps  #decorator function

app=Flask(__name__)
app.secret_key='kkkl'

bcrypt=Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')


def login_required(f):
    @wraps(f)
    def protected(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected 


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
        
        new_product=(productName,buying_price,selling_price)
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
    stock_available=available_stock(productsid)
    if stock_available < float(quantity):
        flash("Insufficient stock","info")
    insert_sales(new_sale)
    flash("sale succesfully made","success")
    return redirect(url_for('sales'))

@app.route('/dashboard')
@login_required
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



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        firstname=request.form['f_name']
        lastname=request.form['l_name']
        email=request.form['email']
        phone_number=request.form['p_num']
        password=request.form['pass']

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        user=check_user(email)
        
        if not user:
            new_user=(firstname,lastname,email,phone_number,hashed_password)
            insert_users(new_user)
            return redirect(url_for('login'))
        else:
            print('Already Registered')
    return render_template('register2.html')        
            
        
@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['passw']
        print(email)

        user=check_user(email)


        
        if not user:
            flash("User not found, please register","error")
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[-1],password):
                flash("Logged in","success")
                session['email'] = email
                
                return redirect(url_for('dashboard'))
            else:
                flash("Passwords mismatch","error")
                # print('passwords mismatch')
                return redirect(url_for('login'))
                
    return render_template('login.html')

@app.route('/stock')
def stock():
    products=fetch_products()
    stock=fetch_stock()
    return render_template('stock.html',products=products,stock=stock)

@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    if request.method=='POST':
        pid=request.form['pid']
        quantity=request.form['quantity']
        new_stock=(pid,quantity)
        insert_stock(new_stock)
        flash("stock added succesfully","success")
        return redirect(url_for('stock'))
    

        



app.run(debug=True)