#!/bin/sh

# Script para crear superusuario de Django usando variables de entorno
# Las variables requeridas: SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD

# Validar que existan las variables requeridas
if [ -z "$SUPERUSER_USERNAME" ] || [ -z "$SUPERUSER_EMAIL" ] || [ -z "$SUPERUSER_PASSWORD" ]; then
    echo "⚠️  ADVERTENCIA: No se encontraron todas las variables de entorno requeridas para crear el superusuario."
    echo "   Variables requeridas: SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD"
    echo "   Por favor, configure estas variables en el archivo .env o en el entorno del contenedor."
    echo "   El superusuario NO fue creado automáticamente. Debe crearlo manualmente con:"
    echo "   python manage.py createsuperuser"
    exit 0
fi

# Verificar si ya existe el superusuario
echo "Verificando si existe el superusuario '$SUPERUSER_USERNAME'..."
python3 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    print('El superusuario ya existe, omitiendo creación.')
    exit(0)
else:
    print('Creando superusuario...')
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print('Superusuario creado exitosamente.')
" 2>/dev/null || {
    echo "Error al crear el superusuario. Verifique las credenciales."
    exit 1
}

echo "Proceso de creación de superusuario completado."