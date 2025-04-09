from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime
from zoneinfo import ZoneInfo

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

            # 1. Update the appointment's status to 'Completed'
            cursor.execute(
                "UPDATE appointment SET status = %s WHERE appointment_id = %s",
                ('Completed', appointment_id)
            )

            # 2. Get the blood type and quantity of this appointment
            cursor.execute("""
                SELECT 
                    b.blood_type_name, 
                    a.quantity
                FROM 
                    appointment a
                JOIN 
                    blood_type b ON a.blood_type_id = b.blood_type_id
                WHERE 
                    a.appointment_id = %s
            """, (appointment_id,))
            blood_type_data = cursor.fetchone()

            if blood_type_data:
                blood_type_name = blood_type_data[0]
                quantity = blood_type_data[1]

                # 3. Get current time in Philippine timezone
                ph_time = datetime.now(ZoneInfo("Asia/Manila"))
                formatted_date = ph_time.strftime("%Y-%m-%d %I:%M:%S %p")

                # 4. Insert into inventory
                cursor.execute(
                    "INSERT INTO inventory (type, quantity, date) VALUES (%s, %s, %s)",
                    (blood_type_name, quantity, formatted_date)
                )

                conn.commit()
                flash('Appointment is done and inventory updated.', 'success')
            else:
                flash('Appointment not found or invalid.', 'warning')

        except mysql.connector.Error as err:
            flash(f"Database Error: {err}", 'danger')

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return redirect(url_for('main.appointments'))

