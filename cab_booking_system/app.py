from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import random

app = Flask(__name__)
app.secret_key = "cab_secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="654321",   # put your MySQL password if any
    database="cab_booking",
    port=3307
)
cursor = db.cursor()

# ================= ROLE SELECTION =================
@app.route('/')
def select_role():
    return render_template('select_role.html')

# ================= USER LOGIN =================
@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        phone = request.form['phone']
        otp = str(random.randint(1000,9999))
        session['otp'] = otp
        session['phone'] = phone

        cursor.execute(
            "INSERT INTO users (phone, otp) VALUES (%s,%s) ON DUPLICATE KEY UPDATE otp=%s",
            (phone, otp, otp)
        )
        db.commit()
        return redirect('/verify')

    return render_template('user_login.html')

@app.route('/verify', methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        if request.form['otp'] == session['otp']:
            cursor.execute("SELECT user_id FROM users WHERE phone=%s", (session['phone'],))
            user = cursor.fetchone()
            session['user_id'] = user[0]
            return redirect('/dashboard')
        return "Invalid OTP"

    return render_template('verify.html')

# ================= USER DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM cabs")
    cabs = cursor.fetchall()
    return render_template('user_dashboard.html', cabs=cabs)

@app.route('/book_cab', methods=['POST'])
def book_cab():
    pickup = request.form['pickup']
    drop = request.form['drop']
    distance = float(request.form['distance'])
    cab_type = request.form['cab_type']
    user_id = session['user_id']

    cursor.execute("SELECT base_fare, per_km FROM cabs WHERE cab_type=%s", (cab_type,))
    cab = cursor.fetchone()
    fare = cab[0] + (cab[1] * distance)

    cursor.execute("""
        INSERT INTO bookings
        (user_id, driver_id, pickup, drop_location, cab_type, distance, fare, status)
        VALUES (%s,1,%s,%s,%s,%s,%s,'Booked')
    """, (user_id, pickup, drop, cab_type, distance, fare))
    db.commit()

    return f"Cab booked successfully! Fare: ₹{fare}"

# ================= DRIVER REGISTER =================
@app.route('/driver_register', methods=['GET','POST'])
def driver_register():
    if request.method == 'POST':
        cursor.execute("""
            INSERT INTO drivers
            (name, phone, password, cab_type, latitude, longitude, status)
            VALUES (%s,%s,%s,%s,0,0,'Available')
        """, (
            request.form['name'],
            request.form['phone'],
            request.form['password'],
            request.form['cab_type']
        ))
        db.commit()
        return redirect('/driver_login')

    return render_template('driver_register.html')

# ================= DRIVER LOGIN =================
@app.route('/driver_login', methods=['GET','POST'])
def driver_login():
    if request.method == 'POST':
        cursor.execute(
            "SELECT driver_id FROM drivers WHERE phone=%s AND password=%s",
            (request.form['phone'], request.form['password'])
        )
        driver = cursor.fetchone()
        if driver:
            session['driver_id'] = driver[0]
            return redirect('/driver_dashboard')
        return "Invalid driver credentials"

    return render_template('driver_login.html')

# ================= DRIVER DASHBOARD =================
@app.route('/driver_dashboard')
def driver_dashboard():
    return render_template('driver_dashboard.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    cursor.execute(
        "UPDATE drivers SET latitude=%s, longitude=%s WHERE driver_id=%s",
        (request.form['lat'], request.form['lng'], session['driver_id'])
    )
    db.commit()
    return "Location Updated"

@app.route('/get_driver_location')
def get_driver_location():
    cursor.execute("SELECT latitude, longitude FROM drivers WHERE driver_id=1")
    loc = cursor.fetchone()
    return jsonify({'lat': loc[0], 'lng': loc[1]})

if __name__ == "__main__":
    app.run(debug=True)
