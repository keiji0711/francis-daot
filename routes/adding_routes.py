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
        bloodType = request.form.get('blood_type')
        location = request.form['location']
        purpose = request.form['purpose']

        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO appointment (donor_id,date,blood_type_id,location,purpose,status) VALUES (%s, %s, %s, %s, %s, %s)""",
                           (donor_name, date, bloodType, location, purpose, 'Active'))
            conn.commit()
            flash('Appointment added successfully', 'success')

        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return redirect(url_for('main.appointments'))