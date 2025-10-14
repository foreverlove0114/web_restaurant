from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from online_restaurant_db import Session, Reservation
from datetime import datetime
import logging

reservations_bp = Blueprint('reservations', __name__)

logger = logging.getLogger(__name__)


@reservations_bp.route('/reserved', methods=['GET', 'POST'])
@login_required
def reserved():
    if request.method == "POST":
        logger.info(f"Form data: {request.form}")
        logger.info(f"User {current_user.id} attempting reservation")
        logger.info(f"User {current_user.id} submitted reservation form")

        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.warning(f"CSRF token mismatch for user {current_user.id}")
            return "Request blocked!", 403

        try:
            table_type = request.form['table_type']
            reserved_time_str = request.form['time']

            # 将字符串时间转换为 datetime 对象
            try:
                # 假设时间格式为 "YYYY-MM-DDTHH:MM" (HTML datetime-local 输入)
                reserved_time = datetime.strptime(reserved_time_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                # 如果格式不匹配，尝试其他常见格式
                try:
                    reserved_time = datetime.strptime(reserved_time_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    flash('Invalid time format. Please use the date picker.', 'error')
                    logger.error(f"Invalid time format: {reserved_time_str}")
                    return render_template('reservation/reserved.html', csrf_token=session["csrf_token"],
                                           active_page='reservations')

            logger.info(f"User {current_user.id} tries to reserve table type {table_type} at {reserved_time}")

            with Session() as cursor:
                # 检查用户是否已有预约
                user_reserved_check = cursor.query(Reservation).filter_by(user_id=current_user.id).first()
                if user_reserved_check:
                    logger.warning(f"User {current_user.id} already has an active reservation")
                    flash('You can have only one active reservation.', 'warning')
                    return render_template('reservation/reserved.html', csrf_token=session["csrf_token"],
                                           active_page='reservations')

                # 检查该时间段该桌型是否已被预约
                existing_reservation = cursor.query(Reservation).filter_by(
                    time_start=reserved_time,
                    type_table=table_type
                ).first()

                if existing_reservation:
                    logger.warning(f"Reservation unavailable: table {table_type} at {reserved_time} already taken")
                    flash('Unfortunately, a reservation for this type of table is currently not available.', 'warning')
                    return render_template('reservation/reserved.html', csrf_token=session["csrf_token"],
                                           active_page='reservations')

                # 创建新预约
                new_reservation = Reservation(
                    type_table=table_type,
                    time_start=reserved_time,
                    user_id=current_user.id
                )
                cursor.add(new_reservation)
                cursor.commit()

                logger.info(f"Reservation created: user {current_user.id}, table {table_type}, time {reserved_time}")
                flash(
                    f'Reservation for {reserved_time.strftime("%Y-%m-%d %H:%M")} for a {table_type}-person table successfully created!',
                    'success')

                return redirect(url_for('main.home'))

        except KeyError as e:
            logger.error(f"Missing form field: {e}")
            flash('Please fill in all required fields.', 'error')
        except Exception as e:
            logger.error(f"Error creating reservation: {e}")
            flash('An error occurred while processing your reservation. Please try again.', 'error')

    return render_template('reservation/reserved.html', csrf_token=session["csrf_token"], active_page='reservations')