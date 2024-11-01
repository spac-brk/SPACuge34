import pyodbc
import pandas as pd
import matplotlib.pyplot as plt


# Get query as DataFrame
def df_from_sql(query):
    cursor.execute(query)
    cols = [x[0] for x in cursor.description]
    rows = cursor.fetchall()
    return pd.DataFrame.from_records(rows, columns=cols)


# Specifying the ODBC driver, server name, database, etc. directly
cnxn = pyodbc.connect('DRIVER={MySQL ODBC 8.0 ANSI Driver};SERVER=localhost;DATABASE=northwind;UID=brk;PWD=12345678')

# Create a cursor from the connection
cursor = cnxn.cursor()

# Encoding and decoding
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(encoding='utf-8')

# Sales per ShipCountry
country_sales_s = df_from_sql("""
select sum(orderdetails.Quantity*orderdetails.UnitPrice) as Sales,Orders.ShipCountry
  from orderdetails left join orders
    on orderdetails.OrderID = orders.orderID
group by orders.ShipCountry
order by Sales desc;
""")

# Sales per ShipCountry, more pandas, less sql
country_sales_p = df_from_sql("""
select orderdetails.Quantity,orderdetails.UnitPrice,Orders.ShipCountry
  from orderdetails left join orders on orderdetails.OrderID = orders.orderID;
""")

country_sales_p['Sales'] = country_sales_p['Quantity'] * country_sales_p['UnitPrice']
country_sales_p = ((country_sales_p[['ShipCountry', 'Sales']]
                    .groupby(by='ShipCountry'))['Sales']
                   .sum().sort_values(ascending=False).reset_index())

# Sales per Supplier
supplier_sales = df_from_sql("""
select sum(orderdetails.Quantity*orderdetails.UnitPrice) as Sales,suppliers.CompanyName
  from orderdetails left join (products left join suppliers
    on products.SupplierID = suppliers.SupplierID)
    on orderdetails.ProductID = products.ProductID
group by suppliers.SupplierID
order by Sales desc;
""")

# Plotting
fig1, ax1 = plt.subplots()
plt.subplots_adjust(bottom=0.3)

ax1.bar(country_sales_s['ShipCountry'], country_sales_s['Sales'])
ax1.set_ylabel('Sales')
ax1.set_xlabel('Country')
ax1.set_title('Sales per Country')
ax1.set_xticks(country_sales_s['ShipCountry'], rotation=45, ha='right', labels=country_sales_s['ShipCountry'])

fig2, ax2 = plt.subplots()
plt.subplots_adjust(bottom=0.3)

ax2.bar(country_sales_p['ShipCountry'], country_sales_p['Sales'])
ax2.set_ylabel('Sales')
ax2.set_xlabel('Country')
ax2.set_title('Sales per Country')
ax2.set_xticks(country_sales_p['ShipCountry'], rotation=45, ha='right', labels=country_sales_p['ShipCountry'])

fig3, ax3 = plt.subplots()
plt.subplots_adjust(bottom=0.45)

ax3.bar(supplier_sales['CompanyName'], supplier_sales['Sales'])
ax3.set_ylabel('Sales')
ax3.set_ylabel('Supplier')
ax3.set_title('Sales per Supplier')
ax3.set_xticks(supplier_sales['CompanyName'], rotation=90, ha='center', labels=supplier_sales['CompanyName'])

plt.show()
