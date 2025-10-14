from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import login_required, current_user
from online_restaurant_db import Session, Menu, Role, Reservation, Users, Orders
import logging
import os
import uuid

admin_bp = Blueprint('admin', __name__)

logger = logging.getLogger(__name__)

@admin_bp.route("/add_position", methods=['GET', 'POST'])
@login_required
def add_position():
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            logger.warning(f"Unauthorized access attempt by user {current_user.id} to add_position")
            flash("Access denied! Only administrators can add new items.", "error")
            return redirect(url_for('main.home'))

    if request.method == "POST":
        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.error(f"CSRF token mismatch by user {current_user.id} in add_position")
            return "Request blocked!", 403

        name = request.form['name']
        file = request.files.get('img')
        ingredients = request.form['ingredients']
        description = request.form['description']
        price = request.form['price']
        weight = request.form['weight']

        if not file or not file.filename:
            logger.error(f"User {current_user.id} failed to upload file for new position {name}")
            return 'No file selected or upload failed.'

        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        output_path = os.path.join('static/menu', unique_filename)

        with open(output_path, 'wb') as f:
            f.write(file.read())

        with Session() as cursor:
            new_position = Menu(
                name=name,
                ingredients=ingredients,
                description=description,
                price=int(price),
                weight=weight,
                file_name=unique_filename
            )
            cursor.add(new_position)
            cursor.commit()

        logger.info(f"User {current_user.id} added new menu position '{name}' successfully")
        flash('Item added successfully!', 'success')
        return render_template('admin/add_position.html', csrf_token=session["csrf_token"])

    return render_template('admin/add_position.html', csrf_token=session["csrf_token"])


@admin_bp.route("/edit_position/<id>", methods=['GET', 'POST'])
@login_required
def edit_position(id):
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            logger.warning(f"Unauthorized access attempt by user {current_user.id} to edit_position {id}")
            flash("Access denied! Only administrators can edit menu.", "error")
            return redirect(url_for('main.home'))
        us_position = cursor.query(Menu).filter_by(active=True, id=id).first()

    if request.method == "POST":
        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.error(f"CSRF token mismatch by user {current_user.id} in edit_position {id}")
            return "Request blocked!", 403

        new_name = request.form.get('name') or us_position.name
        new_file = request.files.get('img')
        new_ingredients = request.form.get('ingredients') or us_position.ingredients
        new_description = request.form.get('description') or us_position.description
        new_price = request.form.get('price') or us_position.price
        new_weight = request.form.get('weight') or us_position.weight

        unique_filename = us_position.file_name

        if new_file and new_file.filename:
            old_path = os.path.join('static/menu', us_position.file_name)
            if os.path.exists(old_path):
                os.remove(old_path)

            unique_filename = f"{uuid.uuid4()}_{new_file.filename}"
            output_path = os.path.join('static/menu', unique_filename)
            new_file.save(output_path)

        with Session() as cursor:
            us_position = cursor.query(Menu).filter_by(active=True, id=id).first()
            us_position.name = new_name
            us_position.file_name = unique_filename
            us_position.ingredients = new_ingredients
            us_position.description = new_description
            us_position.price = new_price
            us_position.weight = new_weight
            cursor.commit()

        logger.info(f"User {current_user.id} edited menu position {id} successfully")
        flash('Position successfully edited!', 'success')
        return redirect(url_for('menu.show_menu'))

    return render_template('admin/edit_position.html', csrf_token=session["csrf_token"], us_position=us_position)


@admin_bp.route('/reservations_check', methods=['GET', 'POST'])
@login_required
def reservations_check():
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            logger.warning(f"Unauthorized access attempt by user {current_user.id} to reservations_check")
            flash("Access denied! Only administrators can check reservations.", "error")
            return redirect(url_for('main.home'))

    if request.method == "POST":
        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.error(f"CSRF token mismatch by user {current_user.id} in reservations_check")
            return "Request blocked!", 403

        reserv_id = request.form['reserv_id']
        with Session() as cursor:
            reservation = cursor.query(Reservation).filter_by(id=reserv_id).first()
            cursor.delete(reservation)
            cursor.commit()
        logger.info(f"User {current_user.id} deleted reservation {reserv_id}")

    with Session() as cursor:
        all_reservations = cursor.query(Reservation).all()
        return render_template(
            'admin/reservations_check.html',
            all_reservations=all_reservations,
            csrf_token=session["csrf_token"]
        )


@admin_bp.route('/menu_check', methods=['GET', 'POST'])
@login_required
def menu_check():
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            logger.warning(f"Unauthorized access attempt by user {current_user.id} to menu_check")
            flash("Access denied! Only administrators can check menu.", "error")
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        if request.form.get("csrf_token") != session['csrf_token']:
            logger.error(f"CSRF token mismatch by user {current_user.id} in menu_check")
            return "Request blocked!", 403

        position_id = request.form['pos_id']
        with Session() as cursor:
            position_obj = cursor.query(Menu).filter_by(id=position_id).first()
            if 'change_status' in request.form:
                position_obj.active = not position_obj.active
                logger.info(f"User {current_user.id} toggled status of menu position {position_id}")
            elif 'delete_position' in request.form:
                cursor.delete(position_obj)
                logger.info(f"User {current_user.id} deleted menu position {position_id}")
            elif 'change_position' in request.form:
                logger.info(f"User {current_user.id} started editing menu position {position_id}")
                return redirect(url_for('admin.edit_position', id=position_id))
            cursor.commit()

    with Session() as cursor:
        all_positions = cursor.query(Menu).all()
    return render_template('admin/check_menu.html', all_positions=all_positions, csrf_token=session["csrf_token"])


@admin_bp.route('/all_users')
@login_required
def all_users():
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            logger.warning(f"Unauthorized access attempt by user {current_user.id} to all_users")
            flash("Access denied! Only administrators can check all users.", "error")
            return redirect(url_for('main.home'))

    with Session() as cursor:
        all_users = cursor.query(Users).all()
    logger.info(f"User {current_user.id} viewed all users list")
    return render_template('admin/all_users.html', all_users=all_users)


@admin_bp.route('/order_management')
@login_required
def order_management():
    # 检查管理员权限
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            flash("Access denied! Only administrators can manage orders.", "error")
            return redirect(url_for('main.home'))

    with Session() as cursor:
        # 获取所有订单，按时间倒序排列
        all_orders = cursor.query(Orders).order_by(Orders.order_time.desc()).all()

        # 处理订单数据用于显示
        processed_orders = []
        for order in all_orders:
            try:
                order_data = json.loads(order.order_list) if isinstance(order.order_list, str) else order.order_list
            except:
                order_data = {}

            # 计算订单总价
            order_total = 0
            for item_id, item_data in order_data.items():
                menu_item = cursor.query(Menu).filter_by(id=int(item_id)).first()
                if menu_item:
                    order_total += int(menu_item.price) * int(item_data['num'])

            processed_orders.append({
                'order': order,
                'total_price': order_total,
                'item_count': len(order_data),
                'user': cursor.query(Users).filter_by(id=order.user_id).first()
            })

    return render_template('admin/order_management.html',
                           orders=processed_orders,
                           csrf_token=session["csrf_token"])


@admin_bp.route('/activate_order/<int:order_id>', methods=['POST'])
@login_required
def activate_order(order_id):
    # 检查管理员权限
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            return "Access denied!", 403

    if request.form.get("csrf_token") != session["csrf_token"]:
        return "Request blocked!", 403

    with Session() as cursor:
        order = cursor.query(Orders).filter_by(id=order_id).first()
        if order:
            order.status = 'preparing'  # 或者 'active'
            cursor.commit()
            logger.info(f"Admin {current_user.id} activated order {order_id}")
            flash(f"Order #{order_id} has been activated and is now being prepared.", "success")
        else:
            flash("Order not found!", "error")

    return redirect(url_for('admin.order_management'))


@admin_bp.route('/complete_order/<int:order_id>', methods=['POST'])
@login_required
def complete_order(order_id):
    # 类似 activate_order，但将状态改为 'completed'
    # 实现代码类似上面
    with Session() as cursor:
        user_role = cursor.query(Role).filter_by(name="Admin").first()
        if not user_role or current_user.role_id != user_role.id:
            return "Access denied!", 403

    if request.form.get("csrf_token") != session["csrf_token"]:
        return "Request blocked!", 403

    with Session() as cursor:
        order = cursor.query(Orders).filter_by(id=order_id).first()
        if order:
            order.status = 'completed'  # 或者 'active'
            cursor.commit()
            logger.info(f"Admin {current_user.id} activated order {order_id}")
            flash(f"Order #{order_id} has been activated and is now being prepared.", "success")
        else:
            flash("Order not found!", "error")

    return redirect(url_for('admin.order_management'))