from flask import Blueprint, render_template, request, redirect, url_for, flash,redirect
import mysql.connector

bp = Blueprint('adding', __name__, template_folder='templates/admin')

db = {
        'host': 'localhost',
        'user':'root',
        'password':'',
        'database':'blood_donation'
    }

@bp.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        donor_name = request.form.get('donor_name')
        date = request.form['appointmentDate']
        location = request.form['location']
        purpose = request.form['purpose']
        quantity = request.form['quantity']

        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()

            cursor.execute("""SELECT donors.donor_name, blood_type.blood_type_id
FROM donors
JOIN blood_type ON donors.blood_type_id = blood_type.blood_type_id
WHERE donors.donor_id = %s""", (donor_name,))
            blood_type_id = cursor.fetchone()

            cursor.execute("""INSERT INTO appointment (donor_id,date,blood_type_id,location,purpose,quantity,status) VALUES (%s, %s, %s, %s, %s, %s,%s)""",
                           (donor_name, date, blood_type_id[1], location, purpose, quantity, 'Active'))
            conn.commit()
            flash('Appointment added successfully', 'success')

        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return redirect(url_for('main.appointments'))