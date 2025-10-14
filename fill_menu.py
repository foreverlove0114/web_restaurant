import os
import shutil
import uuid
import requests
from online_restaurant_db import Session, Menu, Base, engine, Role

Base.metadata.create_all(engine)

def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

def add_dish(name, weight, ingredients, description, price, image_url):
    unique_filename = f"{uuid.uuid4()}_{name.replace(' ', '_')}.jpg"
    output_path = os.path.join('static/menu', unique_filename)

    if download_image(image_url, output_path):
        with Session() as cursor:
            new_position = Menu(
                name=name,
                weight=weight,
                ingredients=ingredients,
                description=description,
                price=price,
                file_name=unique_filename,
                active=True
            )
            cursor.add(new_position)
            cursor.commit()
            print(f"Added dish: {name}")
    else:
        print(f"Failed to add dish: {name}")

if not os.path.exists('static/menu'):
    os.makedirs('static/menu')

dishes = [
    {
        "name": "Margherita",
        "weight": "450",
        "ingredients": "Dough, tomato sauce, mozzarella, basil, olive oil",
        "description": "Classic Italian pizza with delicate tomato sauce, fresh mozzarella and aromatic basil. Perfect choice for lovers of traditional Italian cuisine.",
        "price": 180,
        "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Pepperoni",
        "weight": "480",
        "ingredients": "Dough, tomato sauce, mozzarella, pepperoni, oregano",
        "description": "Pizza with spicy pepperoni sausages, juicy tomato sauce and stretchy mozzarella. Experience the real American taste!",
        "price": 210,
        "image_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Carbonara",
        "weight": "320",
        "ingredients": "Pasta, bacon, cream, eggs, parmesan, black pepper",
        "description": "Incredibly delicious pasta with delicate cream sauce, crispy bacon and aromatic parmesan. Prepared according to traditional Italian recipe.",
        "price": 160,
        "image_url": "https://images.unsplash.com/photo-1612874742237-6526221588e3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Caesar with Chicken",
        "weight": "250",
        "ingredients": "Romaine lettuce, chicken fillet, parmesan, croutons, caesar sauce",
        "description": "Fresh romaine lettuce, tender chicken fillet, crispy croutons and signature caesar sauce. Perfect choice for a light and tasty lunch.",
        "price": 150,
        "image_url": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Ukrainian Borscht",
        "weight": "400",
        "ingredients": "Beef, beets, cabbage, potatoes, carrots, onions, tomato paste, sour cream",
        "description": "Traditional Ukrainian borscht with aromatic beef and fresh vegetables. Served with sour cream and garlic bread.",
        "price": 120,
        "image_url": "https://images.unsplash.com/photo-1594283255808-ee6b56142eb7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Ribeye Steak",
        "weight": "350",
        "ingredients": "Ribeye beef, spices, butter, rosemary",
        "description": "Juicy steak from marbled beef, grilled to perfect doneness. Served with butter and fresh herbs.",
        "price": 350,
        "image_url": "https://images.unsplash.com/photo-1600891964092-4316c288032e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Tiramisu",
        "weight": "150",
        "ingredients": "Savoiardi cookies, mascarpone, coffee, cocoa, eggs, sugar",
        "description": "Classic Italian dessert with delicate mascarpone cream, coffee-soaked cookies and cocoa. Perfect ending to your meal.",
        "price": 120,
        "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Sushi Set 'Philadelphia'",
        "weight": "500",
        "ingredients": "Rice, salmon, cream cheese, avocado, cucumber, nori",
        "description": "Set of 24 sushi pieces, including popular Philadelphia, California and Dragon rolls. Served with ginger, wasabi and soy sauce.",
        "price": 450,
        "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Greek Salad",
        "weight": "230",
        "ingredients": "Tomatoes, cucumbers, bell peppers, red onions, olives, feta, olive oil, oregano",
        "description": "Fresh salad with juicy vegetables, olives and feta cheese, dressed with olive oil and oregano. Taste of sunny Greece on your plate.",
        "price": 140,
        "image_url": "https://images.unsplash.com/photo-1599021419847-d8a7a6aba5b7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Cheeseburger",
        "weight": "320",
        "ingredients": "Bun, beef patty, cheddar cheese, lettuce, tomato, onion, sauce",
        "description": "Juicy burger with beef, melted cheddar cheese and fresh vegetables. Served with french fries and signature sauce.",
        "price": 170,
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Lasagna",
        "weight": "400",
        "ingredients": "Lasagna sheets, beef mince, tomato sauce, béchamel, parmesan",
        "description": "Traditional Italian lasagna with juicy meat bolognese sauce, delicate béchamel sauce and grated parmesan.",
        "price": 190,
        "image_url": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    },
    {
        "name": "Cherry Dumplings",
        "weight": "250",
        "ingredients": "Dough, cherries, sugar, sour cream",
        "description": "Homemade dumplings with juicy cherries, served with sour cream and powdered sugar. Traditional Ukrainian dessert.",
        "price": 110,
        "image_url": "https://images.unsplash.com/photo-1590498418987-12d9a8498799?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    }
]

def setup_menu():
    for dish in dishes:
        add_dish(
            dish["name"],
            dish["weight"],
            dish["ingredients"],
            dish["description"],
            dish["price"],
            dish["image_url"]
        )

    print("Menu successfully populated!")

def setup_roles():
    with Session() as session:
        if not session.query(Role).first():
            session.add_all([
                Role(name="User"),
                Role(name="Admin")
            ])
            session.commit()
            print("User and Admin roles added!")

if __name__ == "__main__":
    setup_menu()

    setup_roles()
    print("Everything is ready!")
