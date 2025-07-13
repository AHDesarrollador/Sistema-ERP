# 🐘 Configuración de PostgreSQL para ERP Dashboard

## 📋 Estado Actual
- **PostgreSQL está instalado** ✅ (versión 16.9)
- **Servicio está activo** ✅
- **Autenticación configurada** ❌ (requiere configuración manual)

---

## 🔧 Configuración Manual Requerida

### 1. **Configurar Usuario PostgreSQL**

Ejecuta estos comandos en tu terminal:

```bash
# Cambiar a usuario postgres
sudo -i -u postgres

# Crear usuario para ERP
createuser --interactive erp_user

# Cuando pregunte:
# - ¿Será el nuevo rol un superusuario? (s/n) n
# - ¿Permitir al nuevo rol crear bases de datos? (s/n) s
# - ¿Permitir al nuevo rol crear más nuevos roles? (s/n) n

# Crear base de datos
createdb -O erp_user erp_dashboard_db

# Configurar contraseña para el usuario
psql
ALTER USER erp_user PASSWORD 'erp_password';
\q

# Salir del usuario postgres
exit
```

### 2. **Configurar Autenticación PostgreSQL**

Edita el archivo de configuración:

```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

Busca las líneas que empiecen con:
```
local   all             all                                     peer
host    all             all             127.0.0.1/32            scram-sha-256
```

Y cámbialas por:
```
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
```

### 3. **Reiniciar PostgreSQL**

```bash
sudo systemctl restart postgresql
```

### 4. **Probar Conexión**

```bash
psql -h localhost -U erp_user -d erp_dashboard_db
# Ingresa la contraseña: erp_password
```

---

## ⚙️ Activar PostgreSQL en Django

Una vez completada la configuración manual:

### 1. **Editar settings.py**

Comenta la configuración SQLite y descomenta PostgreSQL:

```python
# SQLite Configuration (backup)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# PostgreSQL Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}
```

### 2. **Ejecutar Migraciones**

```bash
cd "/home/ariel/Python Project"
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
```

---

## 🧪 Verificar Funcionamiento

### Probar conexión Django:
```bash
python manage.py shell -c "from django.db import connection; connection.cursor().execute('SELECT version()'); print('✅ PostgreSQL conectado!')"
```

### Verificar datos:
```bash
python manage.py shell -c "from apps.users.models import User; print(f'Usuarios: {User.objects.count()}')"
```

---

## 📁 Archivos de Configuración

### **.env** (ya configurado):
```
DATABASE_NAME=erp_dashboard_db
DATABASE_USER=erp_user
DATABASE_PASSWORD=erp_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### **requirements.txt** (ya incluye):
```
psycopg2-binary==2.9.10
```

---

## 🚨 Solución de Problemas

### Error: "role does not exist"
```bash
# Crear usuario manualmente
sudo -i -u postgres
createuser erp_user
```

### Error: "database does not exist"
```bash
# Crear base de datos
sudo -i -u postgres
createdb erp_dashboard_db
```

### Error: "authentication failed"
```bash
# Verificar pg_hba.conf
sudo cat /etc/postgresql/16/main/pg_hba.conf | grep local
```

### Error: "connection refused"
```bash
# Verificar servicio
sudo systemctl status postgresql
sudo systemctl start postgresql
```

---

## ✅ Una vez configurado PostgreSQL

El sistema ERP Dashboard tendrá:
- 🏢 **Base de datos robusta** para producción
- 📊 **Mejor rendimiento** para consultas complejas
- 🔒 **Transacciones ACID** garantizadas
- 📈 **Escalabilidad** para crecimiento futuro

---

*Configuración creada: $(date)*
*Sistema ERP Dashboard - PostgreSQL Setup Guide*