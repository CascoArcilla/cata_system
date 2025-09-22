from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.getenv("SUPERUSER_USERNAME")
email = os.getenv("SUPERUSER_EMAIL")
password = os.getenv("SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuario creado")
else:
    print("Superusuario existente")
