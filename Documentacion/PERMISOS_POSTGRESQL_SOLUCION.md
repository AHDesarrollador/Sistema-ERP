# 🔒 Solución: Permisos PostgreSQL para pgAdmin4

## ❌ **PROBLEMA RESUELTO**

### **Error Original:**
```
ERROR: permission denied for table users_user
SQL state: 42501
```

---

## 🔧 **SOLUCIÓN APLICADA**

### **Permisos Otorgados al Usuario `erp_user`:**

✅ **CONNECT** - Conectar a la base de datos  
✅ **USAGE** - Usar el schema public  
✅ **SELECT** - Leer todas las tablas  
✅ **INSERT** - Insertar datos  
✅ **UPDATE** - Modificar datos  
✅ **DELETE** - Eliminar datos  
✅ **SEQUENCES** - Usar secuencias (IDs auto-incrementales)  
✅ **DEFAULT PRIVILEGES** - Permisos automáticos para tablas futuras  

---

## ✅ **VERIFICACIÓN EXITOSA**

### **Tablas Accesibles:**
- ✅ **users_user:** 2 usuarios
- ✅ **inventory_product:** 5 productos  
- ✅ **inventory_category:** 4 categorías
- ✅ **sales_customer:** 3 clientes

---

## 🚀 **CÓMO USAR PGADMIN4 AHORA**

### **1. Abrir pgAdmin4:**
```bash
/usr/pgadmin4/bin/pgadmin4 &
```

### **2. Conectar al servidor:**
- **Host:** `localhost`
- **Port:** `5432`  
- **Database:** `erp_dashboard_db`
- **Username:** `erp_user`
- **Password:** `erp_password`

### **3. Ver usuarios:**
**Navegar a:**
```
Servers → ERP Dashboard → Databases → erp_dashboard_db → Schemas → public → Tables → users_user
```

**Click derecho en `users_user` → "View/Edit Data" → "All Rows"**

---

## 📊 **CONSULTAS SQL QUE YA FUNCIONAN**

### **Ver todos los usuarios:**
```sql
SELECT 
    id,
    username,
    email,
    first_name,
    last_name,
    is_superuser,
    can_view_dashboard,
    can_manage_inventory,
    can_manage_sales,
    date_joined
FROM users_user 
ORDER BY id;
```

### **Estadísticas de usuarios:**
```sql
SELECT 
    COUNT(*) as total_usuarios,
    COUNT(CASE WHEN is_superuser THEN 1 END) as administradores,
    COUNT(CASE WHEN can_view_dashboard THEN 1 END) as con_dashboard
FROM users_user;
```

### **Ver todos los productos:**
```sql
SELECT 
    id,
    name,
    sku,
    current_stock,
    selling_price,
    category_id
FROM inventory_product;
```

### **Ver todas las categorías:**
```sql
SELECT id, name, description 
FROM inventory_category 
WHERE is_active = true;
```

---

## 🗂️ **TODAS LAS TABLAS DISPONIBLES**

### **Usuarios y Autenticación:**
- `users_user` - Usuarios del sistema
- `users_userprofile` - Perfiles de usuarios  
- `auth_group` - Grupos de permisos
- `auth_permission` - Permisos individuales
- `authtoken_token` - Tokens de API

### **Inventario:**
- `inventory_product` - Productos
- `inventory_category` - Categorías
- `inventory_supplier` - Proveedores
- `inventory_stockmovement` - Movimientos de stock

### **Ventas:**
- `sales_customer` - Clientes
- `sales_sale` - Ventas
- `sales_saleitem` - Items de venta

### **Sistema Django:**
- `django_migrations` - Historial de migraciones
- `django_content_type` - Tipos de contenido
- `django_session` - Sesiones de usuarios

---

## 🛠️ **COMANDOS PARA ADMINISTRAR PERMISOS**

### **Si necesitas otorgar permisos adicionales:**
```sql
-- Conectar como superusuario y ejecutar:
GRANT ALL PRIVILEGES ON DATABASE erp_dashboard_db TO erp_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO erp_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO erp_user;
```

### **Ver permisos actuales:**
```sql
SELECT 
    table_name,
    privilege_type 
FROM information_schema.role_table_grants 
WHERE grantee = 'erp_user' 
AND table_schema = 'public'
ORDER BY table_name;
```

### **Crear nuevo usuario con permisos:**
```sql
CREATE USER nuevo_usuario WITH PASSWORD 'password';
GRANT CONNECT ON DATABASE erp_dashboard_db TO nuevo_usuario;
GRANT USAGE ON SCHEMA public TO nuevo_usuario;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO nuevo_usuario;
```

---

## 🧪 **PROBAR CONEXIÓN**

### **Desde terminal:**
```bash
# Verificar conexión directa
psql -h localhost -U erp_user -d erp_dashboard_db -c "SELECT COUNT(*) FROM users_user;"

# Verificar desde Django
cd "/home/ariel/Python Project"
source venv/bin/activate
python manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT username FROM users_user;')
    print([row[0] for row in cursor.fetchall()])
"
```

---

## 📋 **RESULTADO ESPERADO EN PGADMIN4**

### **Tabla users_user:**
| id | username | email         | is_superuser | can_view_dashboard |
|----|----------|---------------|--------------|-------------------|
| 1  | admin    | admin@erp.com | true         | true              |
| 2  | ariel    |               | false        | false             |

### **Funcionalidades disponibles:**
- ✅ **Ver datos** en todas las tablas
- ✅ **Editar registros** existentes  
- ✅ **Insertar nuevos** registros
- ✅ **Eliminar** registros
- ✅ **Ejecutar consultas SQL** personalizadas
- ✅ **Exportar datos** a CSV/Excel
- ✅ **Ver estructura** de tablas
- ✅ **Analizar índices** y relaciones

---

## 🚨 **TROUBLESHOOTING**

### **Si aún tienes problemas:**

#### **Error de conexión:**
1. Verificar que PostgreSQL esté corriendo:
   ```bash
   sudo systemctl status postgresql
   ```

2. Verificar credenciales en pgAdmin4:
   - Host: `localhost` (no `127.0.0.1`)
   - Puerto: `5432`
   - Usuario: `erp_user`
   - Contraseña: `erp_password`

#### **Error de permisos específicos:**
```sql
-- Reconectar y re-ejecutar permisos
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO erp_user;
```

#### **Tabla no aparece:**
- Refrescar (F5) en pgAdmin4
- Verificar que estás en el schema `public`
- Verificar conexión a base de datos `erp_dashboard_db`

---

## 🎉 **¡POSTGRESQL COMPLETAMENTE ACCESIBLE!**

### **Lo que puedes hacer ahora:**
- 🔍 **Explorar** todos los datos del ERP desde pgAdmin4
- 📊 **Ejecutar consultas** SQL avanzadas  
- 📝 **Modificar datos** directamente en la base de datos
- 📈 **Analizar** estadísticas y reportes
- 🔧 **Administrar** la base de datos gráficamente

**🐘 ¡pgAdmin4 listo para gestionar tu ERP Dashboard!**

*Solución aplicada: $(date)*
*Permisos PostgreSQL → Resuelto ✅*