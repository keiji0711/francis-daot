from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('staff', __name__, template_folder='templates/staff')

@bp.route('/staff/blood_request')
def blood_request():
    return render_template('staff/blood_req.html')