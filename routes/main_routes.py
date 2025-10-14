from flask import Blueprint, render_template, request
from config import TelegramConfig
import requests
import logging
main_bp = Blueprint('main', __name__)

logger = logging.getLogger(__name__)
@main_bp.route('/')
@main_bp.route('/home')
def home():
    return render_template('main/index.html', active_page='home')

@main_bp.route("/about")
def about():
    return render_template('main/about.html', active_page='about')

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        text = f"""
New message from a user!
Name: {name}
Email: {email}
Subject: {subject}
Message: {message}
        """
        url = f"https://api.telegram.org/bot{TelegramConfig.BOT_TOKEN}/sendMessage?chat_id={TelegramConfig.CHAT_ID}&text={text}"
        requests.get(url)
        logger.info(f"User with name {name} and email {email} sent a contact form.")

    return render_template('main/contact.html', active_page='contact')