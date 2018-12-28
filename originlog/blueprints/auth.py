from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    pass
