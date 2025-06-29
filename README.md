**#ERP System (Django)**

A modular, production-grade ERP System built using Django, Django REST Framework, and a layered architecture. The system is designed for multi-organization use and includes inventory management, product tracking, stock movement, user authentication, and more.

#🚀 Features

✅ Modular apps: product, inventory, usermanagement, etc.

✅ UI: HTMX for dynamic UI

✅ Auto timestamping for records


#🛠️ Technologies Used

Python 3.12.4

Django 5.2.3

Django REST Framework

PostgreSQL (SQLite for development)

HTMX (for dynamic UI)

#🧩 Project Structure

erp/
├── manage.py
├── erp/              # Project settings
    ├──services/       # Business logic services (not tied to views)
├── product/           # Product app
├── inventory/         # Inventory app
├── usermanagement/    # User & organization management
├── templates/
└── requirements.txt

#🏗️ Setup Instructions

1. Clone the repo

git clone https://github.com/yourusername/erp.git
cd erp

2. Create and activate a virtual environment

python -m venv erp-env
source erp-env/bin/activate  # On Windows: erp-env\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Apply migrations

python manage.py makemigrations
python manage.py migrate

5. Create a superuser

python manage.py createsuperuser

6. Run the development server

python manage.py runserver

🧪 API and Swagger

Swagger or ReDoc will be auto-generated.

#🧼 Developer Tips

Always run makemigrations after model changes.

Delete __pycache__ folders when resetting the project.

Follow DRY principles using Mixins like UserOrganizationMixin, TimestampedModel.

**#🧠 Author**

Sandip Sharma
