import psycopg2

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

def insert_sales(values):
    insert="insert into sales(productsid,quantity,created_at)values(%s,%s,'now()')"
    cur.execute(insert,values)
    conn.commit()
