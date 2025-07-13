# 👥 Guía: Cómo Ver Usuarios en PostgreSQL

## 📊 **USUARIOS ACTUALES EN EL SISTEMA**

```
ID | Usuario | Email          | Nombre      | Super | Dashboard | Inventario | Ventas | Fecha
---|---------|----------------|-------------|-------|-----------|------------|--------|----------
1  | admin   | admin@erp.com  | Admin User  | Sí    | Sí        | Sí         | Sí     | 2025-07-13
2  | ariel   |                |             | No    | No        | No         | No     | 2025-07-13
```

---

## 🔧 **MÉTODOS PARA VER USUARIOS**

### **1. 🌐 Panel de Administración (MÁS FÁCIL)**

**URL:** http://localhost:8000/admin/users/user/

**Pasos:**
1. Ve a http://localhost:8000/admin/
2. Login con: `admin@erp.com` / `admin123`
3. Click en **"Users"** en la sección "USERS"
4. Verás todos los usuarios con detalles completos

**Ventajas:**
- ✅ Interfaz gráfica completa
- ✅ Puedes editar usuarios
- ✅ Ver todos los permisos
- ✅ Crear nuevos usuarios

---

### **2. 🐍 Django Shell (INTERMEDIO)**

```bash
cd "/home/ariel/Python Project"
source venv/bin/activate
python manage.py shell
```

**Comandos útiles:**
```python
# Ver todos los usuarios
from apps.users.models import User
for user in User.objects.all():
    print(f"{user.username} - {user.email} - Superuser: {user.is_superuser}")

# Contar usuarios
print(f"Total usuarios: {User.objects.count()}")

# Ver usuarios con permisos específicos
admins = User.objects.filter(is_superuser=True)
dashboard_users = User.objects.filter(can_view_dashboard=True)
```

---

### **3. 🗄️ PostgreSQL Directo (AVANZADO)**

```bash
# Conectar directamente a PostgreSQL
psql -h localhost -U erp_user -d erp_dashboard_db

# Consultas SQL directas
SELECT username, email, is_superuser FROM users_user;
SELECT COUNT(*) FROM users_user;
```

---

### **4. 🔗 API REST (PARA DESARROLLADORES)**

**URL:** http://localhost:8000/api/users/list/

**Con autenticación:**
```bash
# Primero obtener token
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@erp.com", "password": "admin123"}'

# Usar token para ver usuarios
curl -H "Authorization: Token TU_TOKEN_AQUI" \
  http://localhost:8000/api/users/list/
```

---

### **5. 💻 Comando Rápido (UNA LÍNEA)**

```bash
cd "/home/ariel/Python Project" && source venv/bin/activate && python manage.py shell -c "
from apps.users.models import User
for u in User.objects.all():
    print(f'{u.id}: {u.username} ({u.email}) - Super: {u.is_superuser} - Dashboard: {u.can_view_dashboard}')
"
```

---

## 📋 **INFORMACIÓN DETALLADA DE USUARIOS**

### **👤 Usuario Admin (ID: 1):**
- **Email:** admin@erp.com
- **Permisos:** Administrador completo
- **Dashboard:** ✅ Acceso total
- **Inventario:** ✅ Gestión completa
- **Ventas:** ✅ Gestión completa

### **👤 Usuario Ariel (ID: 2):**
- **Email:** No configurado
- **Permisos:** Usuario básico
- **Dashboard:** ❌ Sin acceso
- **Inventario:** ❌ Sin acceso
- **Ventas:** ❌ Sin acceso

---

## 🛠️ **GESTIÓN DE USUARIOS**

### **Dar permisos de Dashboard al usuario 'ariel':**
```python
# En Django shell
from apps.users.models import User
user = User.objects.get(username='ariel')
user.can_view_dashboard = True
user.can_manage_inventory = True
user.can_manage_sales = True
user.save()
```

### **Crear nuevo usuario:**
```python
# En Django shell
from apps.users.models import User
new_user = User.objects.create_user(
    username='nuevo_usuario',
    email='nuevo@empresa.com',
    password='password123',
    can_view_dashboard=True
)
```

### **Cambiar contraseña:**
```python
# En Django shell
user = User.objects.get(username='ariel')
user.set_password('nueva_password')
user.save()
```

---

## 📊 **CONSULTAS ÚTILES**

### **Ver usuarios con acceso al dashboard:**
```python
dashboard_users = User.objects.filter(can_view_dashboard=True)
print(f"Usuarios con dashboard: {dashboard_users.count()}")
```

### **Ver administradores:**
```python
admins = User.objects.filter(is_superuser=True)
for admin in admins:
    print(f"Admin: {admin.username} - {admin.email}")
```

### **Ver usuarios creados hoy:**
```python
from datetime import date
today_users = User.objects.filter(date_joined__date=date.today())
print(f"Usuarios creados hoy: {today_users.count()}")
```

---

## 🔍 **ESTRUCTURA DE LA TABLA USERS**

### **Campos principales:**
- `id` - ID único del usuario
- `username` - Nombre de usuario
- `email` - Email (usado para login)
- `first_name` - Nombre
- `last_name` - Apellido
- `is_superuser` - Administrador del sistema
- `is_staff` - Acceso al panel admin
- `can_view_dashboard` - Puede ver dashboard
- `can_manage_inventory` - Puede gestionar inventario
- `can_manage_sales` - Puede gestionar ventas
- `date_joined` - Fecha de creación

---

## 🚀 **RECOMENDACIÓN**

### **Para uso diario:**
👉 **Usa el Panel de Administración** (http://localhost:8000/admin/users/user/)
- Interfaz más fácil y completa
- Puedes editar todo desde el navegador
- No necesitas comandos

### **Para desarrollo:**
👉 **Usa Django Shell** para automatización y scripts

### **Para análisis avanzado:**
👉 **Usa PostgreSQL directo** para consultas complejas

---

**🎯 ¡Ya puedes gestionar todos los usuarios de tu sistema ERP!**

*Guía actualizada: $(date)*