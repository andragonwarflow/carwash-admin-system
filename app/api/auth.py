
from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from app.repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)
user_repo = UserRepository()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = user_repo.authenticate(username, password)
        if user:
            login_user(user)
            return redirect(url_for('api.index'))
        
        flash('Invalid username or password')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
