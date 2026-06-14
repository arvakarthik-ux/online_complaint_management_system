from app import create_app
from app.extensions import db

from app.models.admin import Admin
from app.models import Category

app = create_app()

with app.app_context():

    print("\n==============================")
    print(" CREATE DEPARTMENT ADMIN ")
    print("==============================\n")

    full_name = input("Enter admin name: ").strip()

    username = input("Enter username: ").strip()

    email = input("Enter admin email: ").strip().lower()

    password = input("Enter admin password: ").strip()

    print("\nSelect Role:")
    print("1. Super Admin")
    print("2. Department Admin")

    role_choice = input("\nEnter choice (1 or 2): ").strip()

    if role_choice == "1":

        role = "super_admin"

        category_id = None

    else:

        role = "category_admin"

        categories = Category.query.all()

        if not categories:
            print("\nNo categories found in database.")
            exit()

        print("\nAvailable Departments:\n")

        for c in categories:
            print(f"{c.id}. {c.name}")

        category_id = int(
            input("\nEnter Department ID: ").strip()
        )

    # Check existing email
    existing_email = Admin.query.filter_by(
        email=email
    ).first()

    if existing_email:
        print("\nAdmin email already exists.")
        exit()

    # Check existing username
    existing_username = Admin.query.filter_by(
        username=username
    ).first()

    if existing_username:
        print("\nUsername already exists.")
        exit()

    admin = Admin(

        full_name=full_name,

        username=username,

        email=email,

        role=role,

        category_id=category_id
    )

    admin.set_password(password)

    db.session.add(admin)

    db.session.commit()

    print("\n==============================")
    print(" ADMIN CREATED SUCCESSFULLY ")
    print("==============================")