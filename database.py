import psycopg2
from datetime import datetime

conn=psycopg2.connect(user='postgres',password='leshan1234',host='localhost',port='5432',database='myduka_project'  )

cur=conn.cursor()

def fetch_products():
    cur.execute('select * from products;')
    products=cur.fetchall()
    return products

def fetch_sales():
    cur.execute('select * from sales;')
    sales=cur.fetchall()
    return sales

def insert_products(values):
    insert="insert into products(productName,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

# time=datetime.now()

def insert_sales(values):
    insert="insert into sales(productsid,quantity,created_at)values(%s,%s,now())"
    cur.execute(insert,values)
    conn.commit()

def profit_per_product():
    cur.execute("select products.productname, sum((products.selling_price-products.buying_price)*sales.quantity) as profit from products join sales on products.productsid=sales.productsid group by(products.productName);")
    profit_per_product=cur.fetchall()
    return profit_per_product

profit_product=profit_per_product()
# print(profit_product)

def profit_per_day():
    cur.execute("select date(sales.created_at), sum((products.selling_price-products.buying_price)*sales.quantity) as profit from products join sales on products.productsid=sales.productsid group by (sales.created_at);")
    profit_per_day=cur.fetchall()
    return profit_per_day

profit_day=profit_per_day()
# print(profit_day)


def sales_per_product():
    cur.execute("select products.productname, sum(products.selling_price*sales.quantity) as total_sales from products join sales on products.productsid=sales.productsid group by (products.productname);")
    sales_per_product=cur.fetchall()
    return sales_per_product

sales_product=sales_per_product()
# print(sales_product)

def sales_per_day():
    cur.execute("select date(sales.created_at), sum(products.selling_price*sales.quantity) as total_sales from sales join products on products.productsid=sales.productsid group by(sales.created_at);")
    sales_per_day=cur.fetchall()
    return sales_per_day

sales_day=sales_per_day()
# print(sales_day)


def check_user(email):
    query = "select * from users where email = %s"
    cur.execute(query,(email,))  
    user=cur.fetchone()
    return user 

def insert_users(values):
    insert="insert into users(firstname, lastname, email, phone_number, password)values(%s, %s, %s, %s, %s)"
    cur.execute(insert,values)
    conn.commit()
  


