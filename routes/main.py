from flask import Blueprint, render_template, request, redirect, url_for, flash,session
import mysql.connector
import hashlib



bp = Blueprint('main', __name__, template_folder='templates/admin')

db = {
        'host': 'localhost',
        'user':'root',
        'password':'',
        'database':'blood_donation'
    }

# SHA-256 password hashing function
def hash_password_sha256(password):
    return hashlib.sha256(password.encode()).hexdigest()

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(quantity) AS total_quantity FROM inventory;")
    total_quantity = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM appointment WHERE status = 'Active'")
    total_appointments = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM donors ORDER BY created_at DESC")
    recent_donors = cursor.fetchall()
    recent = []
    if not recent_donors:
        recent = "No recent donors"
    else:
        recent = recent_donors[0]

    cursor.execute("SELECT * FROM inventory ORDER BY date DESC")
    inventory = cursor.fetchall()
    recent_inv = []
    
    if not inventory:
        recent_inv = "None"
    else:
        recent_inv = inventory[0]

    username = session.get('username')
    print(f"Username from session: {username}")  # Debugging print

    return render_template('admin/dashboard.html', username=username, total_donors=total_donors,total_quantity=total_quantity,total_appointments = total_appointments,recent = recent, recent_inv = recent_inv) 

@bp.route('/registered_donors', methods = ['GET', 'POST'])
def registered_donors():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        blood_type = request.form.get('blood_type')
        address = request.form['address']
        contact = request.form['Contact']

        try:
            conn = mysql.connector.connect(**db)
            cursor =  conn.cursor()

            cursor.execute(""" insert into donors(donor_name, donor_age, blood_type_id, address, contact,status)
                            values (%s, %s, %s, %s, %s, %s)""", (name, age, blood_type, address, contact, 'active'))
            conn.commit()
            flash('Donor registered successfully', 'success')

        except mysql.connector.Error as err:
            return f"Error: {err}"
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close

    donors = []
    total_donors = []
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("""SELECT donors.donor_id, donors.donor_name, donors.donor_age,blood_type.blood_type_name,donors.address,
                       donors.contact,donors.status FROM donors,blood_type
            WHERE donors.blood_type_id = blood_type.blood_type_id """)
        donors = cursor.fetchall()

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


    return render_template('admin/registered_donors.html', donors = donors, total_donors = total_donors)

@bp.route('/inventory')
def inventory():
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()
    cursor.execute("""SELECT type, SUM(quantity) AS total_quantity, date
FROM inventory
GROUP BY type""")
    inventory = cursor.fetchall()
    conn.close()
    return render_template('admin/inventory.html', inventory = inventory)

@bp.route('/appointments')
def appointments():
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()

    cursor.execute("select * from donors")
    donors = cursor.fetchall()

    cursor.execute('select * from blood_type')
    blood_type = cursor.fetchall()

    cursor.execute("""SELECT appointment.appointment_id, donors.donor_name,appointment.date, blood_type.blood_type_name,appointment.location,appointment.purpose, appointment.quantity ,appointment.status
FROM appointment,donors, blood_type WHERE appointment.donor_id = donors.donor_id AND appointment.blood_type_id = blood_type.blood_type_id and appointment.status = 'Active' """)
    appointments = cursor.fetchall()
    return render_template('admin/appointment.html', donors = donors, blood_type = blood_type, appointments = appointments)


@bp.route('/blood_requests')
def blood_requests():
    return render_template('admin/blood_requests.html')

@bp.route('/blood_req_transactions')
def blood_req_transactions():
    return render_template('admin/blood_req_transaction.html')

@bp.route('/account_management', methods=['GET', 'POST'])
def account_management():
    if request.method == 'POST':
        username = request.form['username']
        user_type = request.form.get('user_type')
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Print user_type for debugging
        print(user_type)

        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username already exists', 'danger')
                return redirect(url_for('main.account_management'))

            if password == confirm_password:
                # Hash the password with SHA-256
                hashed_password = hash_password_sha256(password)
                
                # Insert the user with the hashed password
                cursor.execute("INSERT INTO user (username, password, type_of_user_id) VALUES (%s, %s, %s)",
                               (username, hashed_password, user_type))
                conn.commit()
                flash('Account created successfully', 'success')
            else:
                flash('Passwords do not match', 'danger')

        except mysql.connector.Error as err:
            return f"Error: {err}"

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

     # Load users to show in table
    users = []
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("""SELECT user.user_id, user.username, type_of_user.user_type, user.password, user.user_id FROM user,
                       type_of_user WHERE user.type_of_user_id = type_of_user.type_of_user_id""")
        users = cursor.fetchall()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return render_template('admin/account_management.html', users = users)

@bp.route('/app_history')
def app_history():
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()

    cursor.execute("""SELECT 
    appointment.appointment_id, 
    donors.donor_name,
    appointment.date, 
    blood_type.blood_type_name, 
    appointment.location, 
    appointment.purpose,
    appointment.quantity,               
    appointment.status
FROM appointment
JOIN donors ON appointment.donor_id = donors.donor_id
JOIN blood_type ON appointment.blood_type_id = blood_type.blood_type_id
WHERE appointment.status != 'Active';
 """)
    app_history = cursor.fetchall()
    return render_template('admin/appointment_history.html', app_history = app_history)
