#Developed by - "Priyanshul Sharma "
# priyanshul.is-a.dev
import mysql.connector as pymysql
from datetime import datetime
passwrd = None
db = None  
C = None

def base_check():
    check = 0
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:

        for i in r:
            if i == 'dealership':
                cursor.execute('USE dealership')
                check = 1
    if check != 1:
        create_database()

def table_check():
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'dealership':
                cursor.execute('USE dealership')
                cursor.execute('SHOW TABLES')
                result = cursor.fetchall()
                if len(result) <= 2:
                    create_tables()
                else:
                    print('      Booting systems...')

def create_database():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS dealership")
        db.commit()
        db.close()
        print("Database 'dealership' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating database: {str(e)}")

def create_tables():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd, database="dealership")
        cursor = db.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                CAR_ID INT PRIMARY KEY,
                MAKE VARCHAR(255),
                MODEL VARCHAR(255),
                YEAR INT,
                PRICE DECIMAL(10, 2),
                AVAILABLE INT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                CUSTOMER_ID INT PRIMARY KEY,
                NAME VARCHAR(255),
                PHONE_NO VARCHAR(15)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                SALE_ID INT AUTO_INCREMENT PRIMARY KEY,
                CUSTOMER_ID INT,
                CAR_ID INT,
                SALE_DATE DATE,
                SALE_PRICE DECIMAL(10, 2),
                FOREIGN KEY (CUSTOMER_ID) REFERENCES customers(CUSTOMER_ID),
                FOREIGN KEY (CAR_ID) REFERENCES cars(CAR_ID)
            )
        """)
        
        db.commit()
        db.close()
        print("Tables 'cars', 'customers', and 'sales' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating tables: {str(e)}")

def QR():
    result = C.fetchall()
    for r in result:
        print(r)
        

def add_car():
    car_id = int(input("Enter Car ID: "))
    make = input("Enter Car Make: ")
    model = input("Enter Car Model: ")
    year = int(input("Enter Year of Manufacture: "))
    price = float(input("Enter Price: "))
    available = int(input("Enter Number of Available Cars: "))
    data = (car_id, make, model, year, price, available)
    sql = "INSERT INTO cars (CAR_ID, MAKE, MODEL, YEAR, PRICE, AVAILABLE) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Car added successfully...')
    except pymysql.Error as e:
        print(f"Error adding car: {str(e)}")

def view_cars():
    C.execute("SELECT * FROM cars")
    QR()

def update_car():
    car_id = int(input("Enter Car ID to update: "))
    field = input("Enter field to update [MAKE, MODEL, YEAR, PRICE, AVAILABLE]: ")
    new_value = input(f"Enter new value for {field}: ")
    if field in ['YEAR', 'AVAILABLE']:
        new_value = int(new_value)
    elif field == 'PRICE':
        new_value = float(new_value)
    sql = f"UPDATE cars SET {field} = %s WHERE CAR_ID = %s"
    try:
        C.execute(sql, (new_value, car_id))
        db.commit()
        print('Car updated successfully...')
    except pymysql.Error as e:
        print(f"Error updating car: {str(e)}")

def delete_car():
    car_id = int(input("Enter Car ID to delete: "))
    sql = "DELETE FROM cars WHERE CAR_ID = %s"
    try:
        C.execute(sql, (car_id,))
        db.commit()
        print('Car deleted successfully...')
    except pymysql.Error as e:
        print(f"Error deleting car: {str(e)}")

def register_customer():
    customer_id = int(input("Enter Customer ID: "))
    name = input("Enter Customer Name: ")
    phone_no = input("Enter Customer Phone Number: ")
    data = (customer_id, name, phone_no)
    sql = "INSERT INTO customers (CUSTOMER_ID, NAME, PHONE_NO) VALUES (%s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Customer registered successfully...')
    except pymysql.Error as e:
        print(f"Error registering customer: {str(e)}")

def view_customers():
    C.execute("SELECT * FROM customers")
    QR()

def record_sale():
    customer_id = int(input("Enter Customer ID: "))
    car_id = int(input("Enter Car ID: "))
    sale_date = datetime.now().date()
    sale_price = float(input("Enter Sale Price: "))
    
    # Check availability
    sql_check = "SELECT AVAILABLE FROM cars WHERE CAR_ID = %s"
    C.execute(sql_check, (car_id,))
    result = C.fetchone()
    if result and result[0] > 0:
        # Record sale
        sql_sale = "INSERT INTO sales (CUSTOMER_ID, CAR_ID, SALE_DATE, SALE_PRICE) VALUES (%s, %s, %s, %s)"
        try:
            C.execute(sql_sale, (customer_id, car_id, sale_date, sale_price))
            # Update car availability
            sql_update = "UPDATE cars SET AVAILABLE = AVAILABLE - 1 WHERE CAR_ID = %s"
            C.execute(sql_update, (car_id,))
            db.commit()
            print('Sale recorded successfully...')
        except pymysql.Error as e:
            print(f"Error recording sale: {str(e)}")
    else:
        print("Car not available.")

def view_sales():
    C.execute("SELECT * FROM sales")
    QR()

def main():
    global passwrd
    passwrd = input("Enter password for MySQL: ")

    base_check()

    table_check()
    
    global db, C
    db = pymysql.connect(host="localhost", user="root", password=passwrd, database="dealership")
    C = db.cursor()
    while True:
        log = input("For Admin: A, For Sales: S ::: ")
        if log.upper() == "A":
            p = input("ENTER ADMIN PASSWORD: ")
            if p == 'admin123':
                print("LOGIN SUCCESSFUL")
                while True:
                    menu = input('''Add Car: AC, View Cars: VC, Update Car: UC, Delete Car: DC, Register Customer: RC, View Customers: VC, Record Sale: RS, View Sales: VS, Exit: X :::''')
                    if menu.upper() == 'AC':
                        add_car()
                    elif menu.upper() == 'VC':
                        view_cars()
                    elif menu.upper() == 'UC':
                        update_car()
                    elif menu.upper() == 'DC':
                        delete_car()
                    elif menu.upper() == 'RC':
                        register_customer()
                    elif menu.upper() == 'VC':
                        view_customers()
                    elif menu.upper() == 'RS':
                        record_sale()
                    elif menu.upper() == 'VS':
                        view_sales()
                    elif menu.upper() == 'X':
                        break
                    else:
                        print("Wrong Input")
                        
        elif log.upper() == "S":
            print("Sales Interface")
            while True:
                menu = input('''Record Sale: RS, View Sales: VS, Exit: X :::''')
                if menu.upper() == 'RS':
                    record_sale()
                elif menu.upper() == 'VS':
                    view_sales()
                elif menu.upper() == 'X':
                    break
                else:
                    print("Wrong Input")

if __name__ == "__main__":
    main()
