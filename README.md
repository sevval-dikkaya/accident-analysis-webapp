# AV Accident Analysis Web App

A Django web application for analyzing and tracking autonomus vehicle accident reports.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sevval-dikkaya/accident-analysis-webapp.git
   cd accident-analysis-webapp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations:**
   This sets up the database structure (tables) on your local machine.
   ```bash
   python manage.py migrate
   ```

## Loading Sample Data

This project includes a sample dataset (`accidents_data.json`) containing accident records and vehicle information. To load this data into your local database:

```bash
python manage.py loaddata accidents_data.json
```

## Running the Application

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   Open your web browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Admin Interface

To access the admin interface to manage accidents and vehicles:

1. **Create a superuser (if you haven't already):**
   ```bash
   python manage.py createsuperuser
   ```

2. **Go to the admin page:**
   [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
