from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector

bp = Blueprint('update', __name__, template_folder='templates/admin')

db = {
        'host': 'localhost',
        'user':'root',
        'password':'',
        'database':'blood_donation'
    }

@bp.route('/update_app_status/<int:appointment_id>', methods=['GET', 'POST'])
def update_app_status(appointment_id):
    if request.method == 'POST':
        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            cursor.execute("UPDATE appointment SET status = %s WHERE appointment_id = %s", ('Completed', appointment_id))
            conn.commit()
            flash('Appointment is done', 'success')
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return redirect(url_for('main.appointments'))


bp.route('/app_history')
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
    appointment.status
FROM appointment
JOIN donors ON appointment.donor_id = donors.donor_id
JOIN blood_type ON appointment.blood_type_id = blood_type.blood_type_id
WHERE appointment.status != 'Active';
 """)
    app_history = cursor.fetchall()
    return render_template('admin/appointment_history.html', app_history = app_history)