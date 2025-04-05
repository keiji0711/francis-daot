from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector

bp = Blueprint('auth', __name__, template_folder='templates/auth')

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/register', methods = ['GET', 'POST'])
def register():

    db = {
        'host': 'localhost',
        'user':'root',
        'password':'',
        'database':'blood_donation'
    }

    if request.method == 'POST':
        username = request.form['username']
        user_type = request.form.get('user_type')
        print(user_type)
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username already exists', 'danger')
                return redirect(url_for('auth.register'))

            if password == confirm_password:
                cursor.execute("INSERT INTO user (username, password, type_of_user_id) VALUES (%s, %s, %s)",
                           (username, password, user_type))
                conn.commit()
            else:
                flash('Passwords do not match', 'danger')

        except mysql.connector.Error as err:
            return f"Error: {err}"
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        return redirect(url_for('main.account_management'))



    return render_template('auth/register.html')