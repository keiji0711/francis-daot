from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector

bp = Blueprint('deletee', __name__, template_folder='templates/admin')

db = {
        'host': 'localhost',
        'user':'root',
        'password':'',
        'database':'blood_donation'
    }

@bp.route('/delete_donor/<int:donor_id>', methods=['POST'])
def delete_donor(donor_id):
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
        conn.commit()
        flash('Donor deleted successfully', 'danger')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
    return redirect(url_for('main.registered_donors'))


@bp.route('/delete_accounts/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE user_id = %s", (account_id,))
        conn.commit()
        flash('Donor deleted successfully', 'danger')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
    return redirect(url_for('main.account_management'))


@bp.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("UPDATE appointment SET status = %s WHERE appointment_id = %s", ('Deleted', appointment_id))
        conn.commit()
        flash('Appointment deleted successfully', 'danger')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
    return redirect(url_for('main.appointments'))