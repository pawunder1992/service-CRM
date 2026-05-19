Garage CRM 🚗
A professional Django-based CRM system designed for auto repair shops to manage workers, clients, and service orders efficiently. 
This project features automated deployment and role-based access control.

🌟 Key Features
Role-Based Access Control:

Admin: Full system access, including the ability to create, edit, and delete any record.

Worker: restricted access. Workers can view their assigned orders but do not have buttons for editing or deleting records.

Automated Environment Setup: 
Initialize the entire database, migrations, and sample data with a single command.

Realistic Sample Data: 
Pre-filled with 50 clients and 100 orders using authentic license plate and phone number formats.

Order Management: 
Track repair categories, assigned performers, and completion status with built-in pagination.

🛠️ Quick Start

1. Create a virtual environment (do not install packages globally in your system):
* **Windows:** `python -m venv .venv`
* **macOS/Linux:** `python3 -m venv .venv`

2. Activate the environment and install only the core packages needed to run the project:
* **Windows (Cmd):** `.venv\Scripts\activate.bat && pip install django`
* **Windows (PowerShell):** `.venv\Scripts\activate.ps1; pip install django`
* **macOS/Linux:** `source .venv/bin/activate && pip install django`

3. Set up the database and migrations:
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py loaddata data.json`
`python create_password.py`

4. Start the Server:
`python manage.py runserver`

🔑 Access Credentials
The following accounts are pre-configured for testing the role-based logic:

**superuser** "Full Access (Create, Edit, Delete)":
* **login**: admin 
* **password**: password123

**user** "Read-Only (CRUD Assigned Tasks only)"
* **login**: worker_1
* **password**: password123