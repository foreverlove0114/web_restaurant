from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from online_restaurant_db import Session, Users, Role
import logging

auth_bp = Blueprint('auth', __name__)

logger = logging.getLogger(__name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.error("CSRF token mismatch in register")
            return "Request blocked!", 403

        nickname = request.form['nickname']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        fullAddress = request.form['fullAddress']

        with Session() as cursor:
            user_role = cursor.query(Role).filter_by(name="User").first()
            if cursor.query(Users).filter_by(email=email).first() or cursor.query(Users).filter_by(nickname=nickname).first():
                logger.warning(f"Register attempt failed: duplicate user with email={email} or nickname={nickname}")
                flash('A user with this email or username already exists!', 'danger')
                return render_template('auth/register.html', csrf_token=session["csrf_token"])

            new_user = Users(
                nickname=nickname,
                email=email,
                contact=contact,
                fullAddress=fullAddress,
                role_id=user_role.id
            )
            new_user.set_password(password)
            cursor.add(new_user)
            cursor.commit()
            cursor.refresh(new_user)
            login_user(new_user)

            logger.info(f"New user registered successfully: id={new_user.id}, nickname={nickname}, email={email}")
            return redirect(url_for('main.home'))

    return render_template('auth/register.html', csrf_token=session["csrf_token"])

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.error("CSRF token mismatch in login")
            return "Request blocked!", 403

        nickname = request.form['nickname']
        password = request.form['password']

        with Session() as cursor:
            user = cursor.query(Users).filter_by(nickname=nickname).first()
            if user and user.check_password(password):
                login_user(user)
                logger.info(f"User logged in successfully: id={user.id}, nickname={nickname}")
                return redirect(url_for('profile.user_profile'))

            logger.warning(f"Failed login attempt for nickname={nickname}")
            flash('Incorrect nickname or password!', 'danger')

    return render_template('auth/login.html', csrf_token=session["csrf_token"])

@auth_bp.route("/logout")
def logout():
    if session.get('basket'):
        session['basket'].clear()
        logger.debug("User basket cleared during logout")

    logout_user()
    logger.info("User logged out successfully")
    return redirect(url_for('main.home'))
