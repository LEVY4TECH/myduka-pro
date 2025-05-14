import psycopg2
from datetime import datetime

conn=psycopg2.connect(user='postgres',password='leshan1234',host='localhost',port='5432',database='mmmyduka'  )

cur=conn.cursor()

def fetch_products():
    cur.execute('select * from productsss;')
    products=cur.fetchall()
    return products

def fetch_sales():
    cur.execute('select * from salesss;')
    sales=cur.fetchall()
    return sales

def fetch_stock():
    cur.execute('select * from stocksss;')
    sales=cur.fetchall()
    return sales


def insert_products(values):
    insert="insert into productsss(name,buying_price,selling_price)values(%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

# time=datetime.now()

def insert_sales(values):
    insert="insert into salesss(pid,quantity,created_at)values(%s,%s,now())"
    cur.execute(insert,values)
    conn.commit()

def add_stock(values):
    insert="insert into stocksss(pid,stock_quantity,created_at)values(%s,%s,now())"
    cur.execute(insert,values)
    conn.commit()

def profit_per_product():
    cur.execute("select productsss.name, sum((productsss.selling_price-productsss.buying_price)*salesss.quantity) as profit from productsss join salesss on productsss.productid=salesss.pid group by(productsss.name);")
    profit_per_product=cur.fetchall()
    return profit_per_product

profit_product=profit_per_product()
# print(profit_product)

def profit_per_day():
    cur.execute("select date(salesss.created_at), sum((productsss.selling_price-productsss.buying_price)*salesss.quantity) as profit from productsss join salesss on productsss.productid=salesss.pid group by (salesss.created_at);")
    profit_per_day=cur.fetchall()
    return profit_per_day

profit_day=profit_per_day()
# print(profit_day)


def sales_per_product():
    cur.execute("select productsss.name, sum(productsss.selling_price*salesss.quantity) as total_sales from productsss join salesss on productsss.productid=salesss.pid group by (productsss.name);")
    sales_per_product=cur.fetchall()
    return sales_per_product

sales_product=sales_per_product()
# print(sales_product)

def sales_per_day():
    cur.execute("select date(salesss.created_at), sum(productsss.selling_price*salesss.quantity) as total_sales from salesss join productsss on productsss.productid=salesss.pid group by(salesss.created_at);")
    sales_per_day=cur.fetchall()
    return sales_per_day

sales_day=sales_per_day()
# print(sales_day)


def check_user(email):
    query = "select * from usersss where email = %s"
    cur.execute(query,(email,))  
    user=cur.fetchone()
    return user 

def insert_users(values):
    insert="insert into usersss(firstname, lastname, email, phone_number, password)values(%s, %s, %s, %s, %s)"
    cur.execute(insert,values)
    conn.commit()
  


