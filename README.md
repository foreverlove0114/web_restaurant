# Flask & Feats - Online Restaurant

A comprehensive web application for an online restaurant developed with Flask. Features user authentication, menu browsing, order management, table reservations, and an admin panel.

## Features

- **User Authentication**: Secure registration and login system with bcrypt password hashing
- **Dish Catalog**: Browse menu with detailed information about each dish including images
- **Search Functionality**: Find dishes by name and ingredients
- **Shopping Cart**: Add dishes to cart and place orders with delivery
- **User Profile Management**: Manage personal information and delivery address
- **Table Reservations**: Book tables for dining in with time and table type selection
- **Order History**: View and track your order history
- **Responsive Design**: User-friendly interface for mobile and desktop devices
- **Admin Panel**: Complete administrative interface for menu management and user oversight
- **Contact Form**: Integrated contact form with Telegram notifications
- **Security Features**: CSRF protection, Content Security Policy, and secure session management

## Dish Details

Each dish in the menu includes:
- Name and weight
- Detailed description
- List of ingredients
- Price
- High-quality image

## Technology Stack

- **Python 3.x**
- **Flask**: Web framework for application development
- **PostgreSQL**: Database for storing information
- **SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **bcrypt**: Secure password hashing
- **HTML/CSS/JavaScript**: Frontend components
- **Blueprint**: Modular project structure
- **Telegram Bot API**: Contact form notifications
- **Content Security Policy**: Enhanced security

## Project Structure

```
FinalFlaskProject/
├── app.py                    # Main application file
├── online_restaurant_db.py   # Database models and configuration
├── config.py                 # Application configuration
├── fill_menu.py             # Menu population script
├── requirements.txt          # Python dependencies
├── routes/                   # Application routes
│   ├── __init__.py
│   ├── auth_routes.py        # Authentication routes
│   ├── main_routes.py        # Main pages (home, about, contact)
│   ├── menu_routes.py        # Menu and dish browsing
│   ├── order_routes.py       # Order management
│   ├── profile_routes.py     # User profile management
│   ├── admin_routes.py       # Administrative functions
│   └── reservations_routes.py # Table reservation system
├── static/                   # Static files
│   ├── css/                  # Stylesheets organized by feature
│   │   ├── admin/           # Admin panel styles
│   │   ├── auth/            # Authentication styles
│   │   ├── main/            # Main page styles
│   │   ├── menu/            # Menu styles
│   │   ├── orders/          # Order styles
│   │   └── reservations/    # Reservation styles
│   ├── js/                  # JavaScript files
│   ├── images/              # General images
│   └── menu/                # Dish images
└── templates/                # HTML templates
    ├── base.html            # Base template
    ├── admin/               # Admin panel templates
    ├── auth/                # Authentication templates
    ├── main/                # Main page templates
    ├── menu/                # Menu templates
    ├── orders/              # Order templates
    └── reservation/         # Reservation templates
```

## Database Models

- **Users**: User accounts with roles (User/Admin)
- **Menu**: Dish information with images
- **Orders**: Order history with JSON order data
- **Reservation**: Table reservations with time slots
- **Role**: User role management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Scrimchic/Flask-Feats.git
   cd Flask-Feats
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # for Linux/Mac
   # or
   .venv\Scripts\activate     # for Windows
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```env
   PGUSER=your_postgres_username
   PGPASS=your_postgres_password
   IP=localhost
   PORT=5432
   DATABASE=restaurant_db
   SECRET_KEY=your_secret_key
   BOT_TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   ```

4. Configure the database:
   ```bash
   python -c "from online_restaurant_db import Base, engine; Base.metadata.create_all(engine)"
   ```

5. Populate the menu with sample data:
   ```bash
   python fill_menu.py
   ```

6. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Register or log in to the system
3. Browse the menu and add dishes to your cart
4. Place an order, specifying the delivery address
5. Make table reservations for dining in
6. Manage your profile and view order history

## Administration

To access administrative functions:
1. Log in with an administrator account
2. Navigate to the admin panel
3. Manage menu items, user accounts, and reservations
4. Add new dishes with images and descriptions

## Security Features

- **Password Hashing**: bcrypt for secure password storage
- **CSRF Protection**: Cross-Site Request Forgery protection
- **Content Security Policy**: Enhanced security headers
- **Session Management**: Secure session handling
- **Input Validation**: Form validation and sanitization

## API Integration

- **Telegram Bot**: Contact form notifications sent to Telegram
- **PostgreSQL**: Robust database backend
- **File Upload**: Secure image upload for menu items

## Author

👨‍💻 **Scrimchic**

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.