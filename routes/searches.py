from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
import mysql.connector

bp = Blueprint('search', __name__, template_folder='templates/admin')

db = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blood_donation'
}


@bp.route('/search_donor')
def search_donor():
    query = request.args.get('q', '')
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()

    # Modify the query to include donor data, filtering based on donor name search
    cursor.execute("""
    SELECT donors.donor_id, donors.donor_name, donors.donor_age, blood_type.blood_type_name, 
           donors.address, donors.contact, donors.status
    FROM donors
    JOIN blood_type ON donors.blood_type_id = blood_type.blood_type_id
    WHERE donors.donor_name LIKE %s
    """, ('%' + query + '%',))

    # Fetch all results from the query
    donors = cursor.fetchall()

    # Convert the result to a list of dictionaries for easier use in the frontend
    results = []
    for donor in donors:
        results.append({
            'donor_id': donor[0],
            'donor_name': donor[1],
            'donor_age': donor[2],
            'blood_type': donor[3],
            'address': donor[4],
            'contact': donor[5],
            'status': donor[6]
        })

    # Close the connection
    cursor.close()
    conn.close()

    # Return the data as JSON
    return jsonify(results)




