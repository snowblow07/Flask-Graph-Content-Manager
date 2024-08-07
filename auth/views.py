from flask import Blueprint, current_app, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from . import models

# Create a Blueprint named 'auth' for the authentication module
auth_bp = Blueprint("auth", __name__)

# Initialize Bcrypt
bcrypt = Bcrypt()

@auth_bp.route('/admin')
def admin():
    return render_template('admin.html')

#@auth_bp.route('/register', methods=['GET', 'POST'])
#@models.check_logged_in
#def register():
#    driver = current_app.config["neo4j_driver"]
#    if request.method == 'POST':
#        username = request.form['username']
#        email = request.form['email']
#        password = request.form['password']
#        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#        if models.create_user(driver, username, email, hashed_password):
#            return redirect(url_for('auth.admin'))  # Ensure 'admin' endpoint exists
#    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@models.check_logged_in
def login():
    driver = current_app.config["neo4j_driver"]
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = models.get_user(driver, username)
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('auth.admin'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.admin'))
