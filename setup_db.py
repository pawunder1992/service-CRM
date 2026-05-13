import os
import django
from django.core.management import call_command

# 1. Setup Django environment
# Ensure 'Garage' matches your project folder name where settings.py is located
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_CRM.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def setup_everything():
    print("🚀 Starting full database automation...")

    # 2. Create migrations (makemigrations)
    try:
        print("1. Creating migration files (makemigrations)...")
        call_command('makemigrations', 'crm')
    except Exception as e:
        print(f"❌ Error during makemigrations: {e}")
        return

    # 3. Run migrations (migrate)
    try:
        print("2. Running migrations (migrate)...")
        call_command('migrate')
    except Exception as e:
        print(f"❌ Error during migrate: {e}")
        return

    # 4. Load data from JSON
    try:
        if os.path.exists('data.json'):
            print("3. Loading data from data.json...")
            call_command('loaddata', 'data.json')
        else:
            print("⚠️ Warning: data.json not found. Skipping data load.")
    except Exception as e:
        print(f"❌ Error during loaddata: {e}")

    # 5. Set passwords for Admin and Worker
    # We use 'admin' and 'worker_1' to match your new generate_data.py script
    password = "password123"
    accounts = [
        {'username': 'admin', 'label': 'Admin'},
        {'username': 'worker_1', 'label': 'First Worker'}
    ]

    print("4. Setting up account passwords...")
    for account in accounts:
        try:
            user = User.objects.get(username=account['username'])
            user.set_password(password)
            user.save()
            print(f"   ✅ Password for {account['label']} ('{user.username}') set to: {password}")
        except User.DoesNotExist:
            print(f"   ❌ User '{account['username']}' not found in database. Check your data.json.")

    print("\n✨ Everything is ready! You can now run: python manage.py runserver")


if __name__ == "__main__":
    setup_everything()