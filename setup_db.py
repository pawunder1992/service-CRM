import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_CRM.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def setup_passwords():
    print("🚀 Starting setting up passwords...")

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


if __name__ == "__main__":
    setup_passwords()