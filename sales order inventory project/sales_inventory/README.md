# Sales Order & Inventory Management System

## Project Overview
This project is built using Django and Django REST Framework to manage dealers, products, inventory, and orders.

## Features
- Dealer Management
- Product Management
- Inventory Tracking
- Create Orders
- Confirm Orders
- Deliver Orders
- Stock Validation

Order Flow:
Draft → Confirmed → Delivered

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite

## Setup Instructions



1. Create virtual environment
python -m venv venv

2. Activate environment
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run migrations
python manage.py makemigrations
python manage.py migrate

5. Run server
python manage.py runserver

Server will run at:
http://127.0.0.1:8000/

6. for creating admin 
python manage.py createsuperuser

## API Endpoints

Create Dealer  
POST /api/dealers/

Create Product  
POST /api/products/

Add Inventory  
POST /api/inventory/

Create Order  
POST /api/orders/

Confirm Order  
POST /api/orders/{id}/confirm/

Deliver Order  
POST /api/orders/{id}/deliver/

## Assumptions
- Only Draft orders can be confirmed
- Only Confirmed orders can be delivered
- Delivered orders cannot be edited