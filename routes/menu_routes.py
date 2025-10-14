from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from online_restaurant_db import Session, Menu
from flask_login import current_user
import logging

menu_bp = Blueprint('menu', __name__)

logger = logging.getLogger(__name__)

@menu_bp.route('/menu')
def show_menu():
    search_query = request.args.get("q", "").strip()

    with Session() as session_db:
        query = session_db.query(Menu).filter_by(active=True)

        if search_query:
            query = query.filter(Menu.name.ilike(f"%{search_query}%"))
            logger.info(f"Menu search performed with query='{search_query}'")

        all_positions = query.all()
        logger.info(f"Menu page loaded, total positions returned: {len(all_positions)}")

    return render_template(
        'menu/menu.html',
        all_positions=all_positions,
        q=search_query,
        active_page='menu'
    )

@menu_bp.route('/position/<int:id>', methods=['GET', 'POST'])
def position(id):
    with Session() as cursor:
        us_position = cursor.query(Menu).filter_by(active=True, id=id).first()
        if not us_position:
            logger.warning(f"Position with id={id} not found")
            flash("Position not found", "error")
            return redirect(url_for("menu.show_menu"))

    if request.method == 'POST':
        if request.form.get("csrf_token") != session["csrf_token"]:
            logger.error(f"CSRF token mismatch while adding position id={id} to basket")
            return "Request blocked!", 403

        position_num = int(request.form.get('num'))
        if current_user.is_authenticated:
            basket = session.get('basket', {})
            basket[str(id)] = {
                "name": us_position.name,
                "num": position_num
            }
            session['basket'] = basket
            flash('Item added to cart!', 'success')
            logger.info(f"User {current_user.id} added position id={id} to basket (num={position_num})")
        else:
            flash('To add an item to the cart, please log in first!', 'warning')
            logger.warning(f"Unauthenticated user attempted to add position id={id} to basket")

    return render_template(
        'menu/position.html',
        csrf_token=session["csrf_token"],
        position=us_position
    )