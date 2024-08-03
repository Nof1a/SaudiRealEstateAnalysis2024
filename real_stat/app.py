from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Rr1223'

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Nouf",
    database="databaserealstate"
)

cursor = db.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Locations (
    region_id INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS RealEstate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region_id INT AUTO_INCREMENT NOT NULL,
    region_name VARCHAR(255),
    month VARCHAR(255),
    property_type VARCHAR(255),
    price_sar DECIMAL(20, 2) NOT NULL,
    area_sqm DECIMAL(20, 2) NOT NULL,
    transaction_count INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Locations(region_id)
)
""")
db.commit()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/employeer')
@app.route('/employeer')
def employeer():
    # List of regions
    regions = [
        (12, 'الباحة'),
        (13, 'الجوف'),
        (9, 'الحدود الشمالية'),
        (1, 'الرياض'),
        (5, 'الشرقية'),
        (4, 'القصيم'),
        (3, 'المدينة'),
        (7, 'تبوك'),
        (10, 'جازان'),
        (8, 'حائل'),
        (6, 'عسير'),
        (2, 'مكة المكرمة'),
        (11, 'نجران')
    ]
    return render_template('employeer.html', regions=regions)


@app.route('/submit_property', methods=['POST'])
def submit_property():
    try:
        # Retrieve and validate form data
        region_name = request.form.get('region', '').strip()
        month = request.form.get('month', '').strip()
        property_type = request.form.get('category', '').strip()
        price = request.form.get('price', '').strip()
        area = request.form.get('area', '').strip()
        deals = request.form.get('deals', '').strip()

        if not (region_name and month and property_type and price and area and deals):
            return "All fields are required!", 400
        
        # Validate price, area, and deals
        try:
            price = float(price)
            area = float(area)
            deals = int(deals)
        except ValueError:
            return "Invalid price, area, or deals number!", 400

        # Check if region exists, if not, create it
        cursor.execute('SELECT region_id FROM Locations WHERE region_name = %s', (region_name,))
        region = cursor.fetchone()
        if not region:
            cursor.execute('INSERT INTO Locations (region_name) VALUES (%s)', (region_name,))
            db.commit()
            cursor.execute('SELECT region_id FROM Locations WHERE region_name = %s', (region_name,))
            region = cursor.fetchone()
        
        region_id = region[0]

        # Insert real estate data
        cursor.execute('''
            INSERT INTO RealEstate (region_id, region_name, month, property_type, price_sar, area_sqm, transaction_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (region_id, region_name, month, property_type, price, area, deals))
        db.commit()
        
        return redirect(url_for('home'))

    except mysql.connector.Error as err:
        return f"Database Error: {err}", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
