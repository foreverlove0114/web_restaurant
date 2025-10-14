from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from online_restaurant_db import Session, Users
import logging

profile_bp = Blueprint('profile', __name__)

logger = logging.getLogger(__name__)

@profile_bp.route("/profile")
def user_profile():
    if current_user.is_authenticated:
        logger.info(f"User {current_user.id} accessed profile page")
        return render_template('auth/profile.html', current_user=current_user, csrf_token=session["csrf_token"])
    logger.warning("Unauthorized access attempt to profile page")
    return redirect(url_for('auth.login'))

@profile_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        logger.warning(f"CSRF token mismatch for user {current_user.id}")
        return "Request blocked!", 403

    old = request.form['oldpassword']
    new = request.form['newpassword']

    with Session() as cursor:
        user = cursor.query(Users).filter_by(id=current_user.id).first()
        if user and user.check_password(old):
            user.set_password(new)
            cursor.commit()
            logger.info(f"User {current_user.id} successfully changed password")
            flash("Password changed successfully!", "success")
        else:
            logger.warning(f"User {current_user.id} failed to change password (old password mismatch)")
            flash("Passwords do not match!", "danger")

    return redirect(url_for('profile.user_profile'))

@profile_bp.route('/change-address', methods=['POST'])
@login_required
def change_address():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        logger.warning(f"CSRF token mismatch for user {current_user.id}")
        return "Request blocked!", 403

    new_address = request.form['new_address']

    with Session() as cursor:
        user = cursor.query(Users).filter_by(id=current_user.id).first()
        if user:
            old_address = user.fullAddress
            user.fullAddress = new_address
            cursor.commit()
            logger.info(f"User {current_user.id} updated address from '{old_address}' to '{new_address}'")
            flash("Address updated successfully!", "success")
        else:
            logger.error(f"User {current_user.id} not found while trying to update address")
            flash("Address does not match!", "danger")

    return redirect(url_for('profile.user_profile'))
