from app import app
from app.database import *
from flask import render_template, request, flash, redirect, url_for, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            if is_valid_user_id(session['user_id']):
                return f(*args, **kwargs) # We found a valid user
        app.logger.warning("No session, this pages requires login")
        flash("This pages requires you to sign-in")
        return redirect(url_for('login'))    
    return decorated_function

@app.route('/')
def homepage():
    return render_template('home.html.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if check_password(username, password):
                flash("Authentication succeeded")
                user_id = get_user_id(username)
                session['user_id'] = user_id
                return redirect(url_for('homepage'))
            else:
                flash("Failed to authenticate")
        
    return render_template('login.html.j2')

@app.route('/logout')
def logout():
    session.clear()
    flash("signed out")
    return redirect(url_for('homepage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            try:
                create_user(username, password)
                flash(f"User '{username}' created")
                return redirect(url_for('homepage'))
            except Exception as ex:
                app.logger.error('Could not register: {}'.format(ex), exc_info=True)
                flash("Failed to register")
       
    return render_template('register.html.j2')

@app.route('/admin')
@login_required
def admin():
    return "Only signed in users can see this"