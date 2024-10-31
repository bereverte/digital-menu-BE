# Digital Menu - Backend

This is the backend for the Digital Menu project, developed with Django.

## Requirements

- Python 3.x
- Git

## Backend Installation (Django)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd digital_menu_backend

2. **Create a virtual environment**:
   python -m venv env

3. **Activate the virtual environment**:
   On Windows: .\env\Scripts\activate
   On macOS/Linux: source env/bin/activate

5. **Install dependencies**:
   pip install -r requirements.txt
   
6. **Apply database migrations**:
   python manage.py migrate

7. **Create a superuser** (optional, for accessing the Django admin panel):
   python manage.py createsuperuser

8. **Run the development server**:
   python manage.py runserver

The server will be available at http://127.0.0.1:8000


## Important Files

- **manage.py**: Main script to run Django commands.
- **requirements.txt**: List of backend dependencies.
- **digital_menu_backend/**: Folder with Django project settings.
- **menu/**: Folder containing the main application for the digital menu.


## Additional Notes

- **Database Configuration**: Currently, the project uses an SQLite database for ease of development. If you need a production database, consider using PostgreSQL or another database system.
- **Environment Variables**: If the project requires environment variables, make sure to add them to a `.env` file (which should be included in `.gitignore`).
