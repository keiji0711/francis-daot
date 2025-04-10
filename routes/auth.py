from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib

bp = Blueprint('auth', __name__, template_folder='templates/auth')

# Database configuration
db = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blood_donation'
}

# SHA-256 password hashing function
def hash_password_sha256(password):
    return hashlib.sha256(password.encode()).hexdigest()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password_sha256(password)

        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                print(f"Found user: {user['username']} with stored password hash: {user['password']}")
                print(f"Hashed input password: {hashed_password}")
                
                if user['password'] == hashed_password:
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['user_type'] = user['type_of_user_id']

                    flash('Logged in successfully!', 'success')  # Set flash message here
                    
                    return redirect(url_for('main.dashboard'))  # Redirect to dashboard after login
                else:
                    print("Password mismatch.")  # Debugging print
            else:
                print("User not found.")  # Debugging print

        except mysql.connector.Error as err:
            return f"Error: {err}"

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('auth/login.html')





# Logout route
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



