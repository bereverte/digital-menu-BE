# Digital Menu - Backend

### Description
**Digital Menu Backend** is a Django-based REST API that powers the **Digital Menu** web application. It provides endpoints for user authentication, restaurant management, menu and category management, and public access to restaurant menus.

### Features:
- **User Authentication**:
  - Token-based authentication.
  - Custom registration endpoint to create restaurant-associated accounts.
- **Restaurant Management**:
  - Manage restaurant details (name, logo, address, contact information).
  - Public endpoint to fetch restaurant details without authentication.
- **Menu Management**:
  - CRUD operations for categories and menu items.
  - Validate menu items to avoid duplicates by name and category.
  - Toggle item availability.
  - Public endpoints to fetch available categories and menu items.
- **Permissions**:
  - Authenticated endpoints for managing restaurant data.
  - Public endpoints for displaying menu information.

### Deployed URL

The backend is deployed at: [Digital Menu Frontend](https://digital-menu-backend-hfa5.onrender.com)


## Project Setup

### Prerequisites

Ensure you have the following installed:

- **Python** (3.8 or later)
- **pip** (Python package manager)
- **PostgreSQL** (optional but recommended for production)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/bereverte/digital-menu-BE.git
   cd digital-menu-BE

2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Create a .env file in the root directory and set the following environment variables:
   ```bash
   SECRET_KEY=your_secret_key
   DEBUG=True   # For production, configure the database (e.g., PostgreSQL) and set DEBUG=False.
   DATABASE_URL=sqlite:///db.sqlite3   # Update this for PostgreSQL in production

5. Apply migrations:
   ```bash
   python manage.py migrate

6. Create a superuser:
   ```bash
   python manage.py createsuperuser

7. Start the development server:
   ```bash
   python manage.py runserver

The backend will be accessible at `http://127.0.0.1:8000`.

## API Documentation

API documentation is available through the following paths:

### Authenticated Endpoints:
- **`/api/restaurants/`**: Manage restaurant details.
- **`/api/categories/`**: Manage categories for menu items.
- **`/api/menuItems/`**: Manage menu items.
- **`/token-auth/`**: Obtain an authentication token.

### Public Endpoints:
- **`/api/restaurants/<id>/public/`**: Fetch restaurant details.
- **`/api/restaurants/<id>/categories/public/`**: Fetch public categories.
- **`/api/restaurants/<id>/menuItems/public/`**: Fetch public menu items.

## Technologies Used:

- **Django**: Python web framework.
- **Django REST Framework (DRF)** for building REST APIs.
- **PostgreSQL**: Recommended for production databases.  
