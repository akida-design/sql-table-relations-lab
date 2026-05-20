# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Boston employees with first name, last name and job title
df_boston = pd.read_sql("""SELECT e.firstName, e.lastName FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'""", conn)

# STEP 2
# Offices with no employees
df_zero_emp = pd.read_sql("""SELECT o.officeCode, o.city, o.country FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL""", conn)

# STEP 3
# All employees with their office city and state, ordered by first then last name
df_employee = pd.read_sql("""SELECT e.firstName, e.lastName, o.city, o.state FROM employees e LEFT
JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName""", conn)

# STEP 4
# Customers with no orders and their sales representative's information
df_contacts = pd.read_sql("""SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL ORDER BY c.contactLastName""", conn)

# STEP 5
# customer contacts with payment info, sorted by amount descending
df_payment = pd.read_sql("""SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber ORDER BY CAST(p.amount AS REAL) DESC""", conn)

# STEP 6
# Top sales reps by average customer credit limit (over 90k)
df_credit = pd.read_sql("""SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(DISTINCT c.customerNumber) AS numCustomers FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber GROUP BY e.employeeNumber,e.firstName, e.lastName HAVING AVG(c.creditLimit) > 90000 ORDER BY numCustomers DESC""", conn)

# STEP 7
# Top selling products by total units sold
df_product_sold = pd.read_sql("""SELECT p.productName, COUNT(DISTINCT o.orderNumber) as numorders, SUM(od.quantityOrdered) AS totalunits FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber GROUP BY p.productCode, p.productName ORDER BY totalUnits DESC""", conn)

# STEP 8
# Products with customer reach count
df_total_customers = pd.read_sql("""SELECT p.productName, p.productCode, COUNT(DISTINCT c.customerNumber) 
                                 AS numpurchasers FROM products p JOIN orderdetails od ON p.productCode = od.productCode JOIN orders o ON od.orderNumber = o.orderNumber JOIN customers c ON o.customerNumber = c.customerNumber GROUP BY p.productCode, p.productName ORDER BY numpurchasers DESC""", conn)

# STEP 9
# Customer count per office
df_customers = pd.read_sql("""SELECT o.officeCode, o.city, COUNT(DISTINCT c.customerNumber) AS n_customers FROM offices o LEFT JOIN employees e ON o.officeCode = e.officeCode LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber GROUP BY o.officeCode, o.city""", conn)

# STEP 10
# Employees who sold underperforming porducts (ordered by fewer than 20 customers)
df_under_20 = pd.read_sql("""WITH underperforming_products AS (SELECT p.productCode FROM products p JOIN
                          orderdetails od ON p.productCode = od.productCode JOIN orders ord ON od.orderNumber = ord.orderNumber GROUP BY 
                          p.productCode HAVING COUNT(DISTINCT ord.customerNumber) < 20) SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, 
                          off.city, off.officeCode FROM employees e JOIN offices off ON e.officeCode = off.officeCode JOIN customers c ON 
                          e.employeeNumber = c.salesRepEmployeeNumber JOIN orders ord ON c.customerNumber = ord.customerNumber JOIN orderdetails 
                          od ON ord.orderNumber = od.orderNumber WHERE od.productCode IN (SELECT productCode FROM underperforming_products) 
                          ORDER BY e.lastName """, conn)
#   Close the connection
conn.close()