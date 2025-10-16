# create_new_admin.py
from online_restaurant_db import Session, Users, Role
import bcrypt


def create_new_admin():
    with Session() as session:
        admin_role = session.query(Role).filter_by(name="Admin").first()

        new_admin = Users(
            nickname="superadmin",
            email="superadmin@restaurant.com",
            contact="+1234567890",
            fullAddress="Admin Address",
            role_id=admin_role.id
        )
        new_admin.set_password("admin123")

        session.add(new_admin)
        session.commit()
        print("New admin user created!")
        print("Username: superadmin")
        print("Password: admin123")


if __name__ == "__main__":
    create_new_admin()