from flask import redirect, render_template, session, url_for
from neo4j import GraphDatabase
from functools import wraps

# Decorator to check if the user is logged in
def check_logged_in(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            # The user is logged in, render a different template
            return render_template('already_authenticated.html')
        return func(*args, **kwargs)
    return decorated_function

# Decorator to check if the user is logged out
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            # The user is not logged in, redirect to the login page
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_function
def create_user(driver, username, email, password):
    with driver.session() as session:
        result = session.run("MATCH (n) WHERE n.username = $username OR n.email = $email RETURN n", username=username, email=email)
        if result.single() is None:
            session.run("CREATE (u:USER {username: $username, email: $email, password: $password})",
                        username=username, email=email, password=password)
            return True
        return False
    
def get_user(driver, username):
    with driver.session() as session:
        result = session.run("MATCH (u:USER {username: $username}) RETURN u", username=username)
        user = result.single()
        if user:
            return user['u']
        return None