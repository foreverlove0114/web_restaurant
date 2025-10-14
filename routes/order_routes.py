from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from online_restaurant_db import Session, Orders, Menu
from datetime import datetime
from config import TelegramConfig
import requests
import logging
import json  # 添加这一行

order_bp = Blueprint('order', __name__)

logger = logging.getLogger(__name__)


@order_bp.route('/create_order', methods=['GET', 'POST'])
def create_order():
    basket = session.get('basket')
    total_price = 0
    if basket:
        with Session() as cursor:
            for item_id, item_data in basket.items():
                menu_item = cursor.query(Menu).filter_by(id=int(item_id)).first()
                if menu_item:
                    total_price += int(menu_item.price) * int(item_data['num'])

    if request.method == 'POST':
        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.error("CSRF token mismatch during order creation")
            return "Request blocked!", 403

        if not current_user.is_authenticated:
            flash("You must be registered to place an order.", 'warning')
            logger.warning("Unauthenticated user attempted to create an order")
            return redirect(url_for('auth.login'))
        else:
            if not basket:
                flash("Your cart is empty.", 'warning')
                logger.warning(f"User {current_user.id} attempted to create an order with empty basket")
            else:
                with Session() as cursor:
                    # 修复：将字典转换为 JSON 字符串
                    order_list_json = json.dumps(basket)

                    new_order = Orders(
                        order_list=order_list_json,  # 使用 JSON 字符串而不是字典
                        order_time=datetime.now(),
                        user_id=current_user.id
                    )
                    cursor.add(new_order)
                    cursor.commit()
                    session.pop('basket')
                    cursor.refresh(new_order)

                    logger.info(f"New order created successfully: id={new_order.id}, user_id={current_user.id}")

                    basket_text = "\n".join(
                        f"{item_data['name']} — {item_data['num']} шт."
                        for item_data in basket.values()
                    )

                    text = f"""
                    New order for user!
                    Id: {current_user.id}
                    Name: {current_user.nickname}
                    Email: {current_user.email}
                    Contact: {current_user.contact}
                    Full Address: {current_user.fullAddress}
                    Order list:
                    {basket_text}
                    """

                    # 添加错误处理到 Telegram 通知
                    try:
                        url = f"https://api.telegram.org/bot{TelegramConfig.BOT_TOKEN}/sendMessage?chat_id={TelegramConfig.CHAT_ID}&text={text}"
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            logger.info(f"Order {new_order.id} notification sent to Telegram")
                        else:
                            logger.warning(
                                f"Failed to send Telegram notification for order {new_order.id}: {response.status_code}")
                    except Exception as e:
                        logger.error(f"Error sending Telegram notification for order {new_order.id}: {e}")

                    return redirect(url_for('order.my_order', id=new_order.id))

    return render_template('orders/create_order.html', csrf_token=session["csrf_token"], basket=basket,
                           total_price=total_price)


@order_bp.route('/my_orders')
@login_required
def my_orders():
    with Session() as cursor:
        us_orders = cursor.query(Orders).filter_by(user_id=current_user.id).all()
        logger.info(f"User {current_user.id} viewed their orders, count={len(us_orders)}")

    return render_template('orders/my_orders.html', us_orders=us_orders)


@order_bp.route("/my_order/<int:id>")
@login_required
def my_order(id):
    with Session() as cursor:
        us_order = cursor.query(Orders).filter_by(id=id, user_id=current_user.id).first()
        if not us_order:
            flash("This order does not exist or it is not yours!", "error")
            logger.warning(f"User {current_user.id} attempted to access non-existing or unauthorized order id={id}")
            return redirect(url_for("order.my_orders"))

        total_price = 0
        # 修复：从 JSON 字符串解析订单数据
        try:
            order_data = json.loads(us_order.order_list) if isinstance(us_order.order_list,
                                                                       str) else us_order.order_list
        except:
            order_data = {}

        for item_id, item_data in order_data.items():
            menu_item = cursor.query(Menu).filter_by(id=int(item_id)).first()
            if menu_item:
                total_price += int(menu_item.price) * int(item_data['num'])

        logger.info(f"User {current_user.id} viewed order id={id}, total_price={total_price}")

    return render_template("orders/my_order.html", order=us_order, total_price=total_price)


@order_bp.route("/cancel_order/<int:id>", methods=["POST", "GET"])
@login_required
def cancel_order(id):
    with Session() as cursor:
        us_order = cursor.query(Orders).filter_by(id=id, user_id=current_user.id).first()
        if us_order:
            cursor.delete(us_order)
            cursor.commit()
            flash("Order deleted!", "success")
            logger.info(f"User {current_user.id} canceled order id={id}")
        else:
            flash("Order not found or it is not yours!", "error")
            logger.warning(f"User {current_user.id} attempted to cancel non-existing or unauthorized order id={id}")

    return redirect(url_for("order.my_orders"))