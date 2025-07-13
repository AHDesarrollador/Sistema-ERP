# 🐘 Guía: Ver Usuarios desde pgAdmin4

## 🚀 **ABRIR PGADMIN4**

### **Método 1: Desde el menú de aplicaciones**
```bash
# Buscar "pgAdmin" en el menú de aplicaciones
# O desde terminal:
pgadmin4
```

### **Método 2: Interfaz web (recomendado)**
```bash
# Abrir en navegador:
http://localhost/pgadmin4
# O si está configurado en puerto específico:
http://localhost:5050
```

---

## 🔗 **CONFIGURAR CONEXIÓN A LA BASE DE DATOS**

### **Paso 1: Crear nueva conexión al servidor**

1. **Abrir pgAdmin4**
2. **Click derecho en "Servers"** → **"Register" → "Server..."**

### **Paso 2: Configurar datos de conexión**

#### **Pestaña "General":**
- **Name:** `ERP Dashboard Local`
- **Server group:** `Servers`

#### **Pestaña "Connection":**
- **Host name/address:** `localhost`
- **Port:** `5432`
- **Maintenance database:** `erp_dashboard_db`
- **Username:** `erp_user`
- **Password:** `erp_password`

#### **Pestaña "Advanced" (opcional):**
- **DB restriction:** `erp_dashboard_db`

### **Paso 3: Guardar conexión**
- ✅ **Save password** (marcar casilla)
- **Click "Save"**

---

## 👥 **VER USUARIOS DE LA APLICACIÓN**

### **Navegación en pgAdmin4:**

```
📂 Servers
 └── 📂 ERP Dashboard Local
     └── 📂 Databases  
         └── 📂 erp_dashboard_db
             └── 📂 Schemas
                 └── 📂 public
                     └── 📂 Tables
                         └── 📋 users_user  ← AQUÍ ESTÁN LOS USUARIOS
```

### **Pasos detallados:**

1. **Expandir servidor:** Click en `ERP Dashboard Local`
2. **Expandir database:** Click en `erp_dashboard_db`  
3. **Expandir Schemas:** Click en `Schemas`
4. **Expandir public:** Click en `public`
5. **Expandir Tables:** Click en `Tables`
6. **Encontrar tabla:** Buscar `users_user`

---

## 📊 **CONSULTAR DATOS DE USUARIOS**

### **Método 1: Ver todos los datos**
1. **Click derecho en `users_user`**
2. **Seleccionar "View/Edit Data"**
3. **Elegir "All Rows"**

### **Método 2: Consulta SQL personalizada**
1. **Click en el icono de SQL** (🔍)
2. **Escribir consulta:**

```sql
-- Ver usuarios básicos
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

### **Método 3: Consulta específica**
```sql
-- Solo usuarios con permisos de dashboard
SELECT username, email, can_view_dashboard 
FROM users_user 
WHERE can_view_dashboard = true;

-- Solo administradores
SELECT username, email, is_superuser 
FROM users_user 
WHERE is_superuser = true;

-- Usuarios creados hoy
SELECT username, email, date_joined 
FROM users_user 
WHERE date_joined::date = CURRENT_DATE;
```

---

## 🗂️ **EXPLORAR TODAS LAS TABLAS DEL ERP**

### **Tablas principales que puedes ver:**

```
📋 users_user           ← Usuarios del sistema
📋 users_userprofile    ← Perfiles de usuarios
📋 inventory_product    ← Productos
📋 inventory_category   ← Categorías
📋 inventory_supplier   ← Proveedores
📋 sales_customer      ← Clientes
📋 sales_sale          ← Ventas
📋 auth_user           ← Usuarios Django (sistema)
📋 authtoken_token     ← Tokens de API
```

### **Para ver cualquier tabla:**
1. **Navegar a:** `Tables` → `nombre_tabla`
2. **Click derecho** → **"View/Edit Data"** → **"All Rows"**

---

## 💡 **CONSULTAS ÚTILES PARA USUARIOS**

### **Estadísticas de usuarios:**
```sql
-- Contar usuarios por tipo
SELECT 
    COUNT(*) as total_usuarios,
    COUNT(CASE WHEN is_superuser THEN 1 END) as administradores,
    COUNT(CASE WHEN can_view_dashboard THEN 1 END) as con_dashboard,
    COUNT(CASE WHEN can_manage_inventory THEN 1 END) as con_inventario
FROM users_user;
```

### **Usuarios con detalles completos:**
```sql
SELECT 
    id,
    username,
    email,
    CONCAT(first_name, ' ', last_name) as nombre_completo,
    CASE 
        WHEN is_superuser THEN 'Administrador'
        WHEN can_view_dashboard THEN 'Usuario Dashboard'
        ELSE 'Usuario Básico'
    END as tipo_usuario,
    date_joined as fecha_registro
FROM users_user
ORDER BY date_joined DESC;
```

### **Actividad reciente:**
```sql
SELECT username, email, last_login, date_joined
FROM users_user 
WHERE date_joined >= NOW() - INTERVAL '7 days'
ORDER BY date_joined DESC;
```

---

## 🛠️ **MODIFICAR USUARIOS DESDE PGADMIN4**

### **⚠️ IMPORTANTE:** 
Solo modifica usuarios desde pgAdmin4 si sabes lo que haces. Es mejor usar el panel de Django admin.

### **Ejemplo - Dar permisos de dashboard:**
```sql
-- Dar acceso al dashboard al usuario 'ariel'
UPDATE users_user 
SET can_view_dashboard = true,
    can_manage_inventory = true,
    can_manage_sales = true
WHERE username = 'ariel';
```

### **Verificar cambio:**
```sql
SELECT username, can_view_dashboard, can_manage_inventory, can_manage_sales
FROM users_user 
WHERE username = 'ariel';
```

---

## 🎯 **DATOS ACTUALES EN TU SISTEMA**

### **Consulta para ver tus usuarios:**
```sql
SELECT 
    id,
    username,
    email,
    CASE WHEN is_superuser THEN '👑 Admin' ELSE '👤 Usuario' END as tipo,
    CASE WHEN can_view_dashboard THEN '✅' ELSE '❌' END as dashboard,
    date_joined::date as fecha
FROM users_user 
ORDER BY id;
```

### **Resultado esperado:**
```
id | username | email         | tipo      | dashboard | fecha
---|----------|---------------|-----------|-----------|------------
1  | admin    | admin@erp.com | 👑 Admin  | ✅        | 2025-07-13
2  | ariel    |               | 👤 Usuario | ❌        | 2025-07-13
```

---

## 🔍 **BUSCAR Y FILTRAR**

### **En la vista de datos:**
- **Filtrar:** Click en el icono de filtro 🔍
- **Ordenar:** Click en los headers de columna
- **Buscar:** Usar la barra de búsqueda

### **Filtros útiles:**
- `is_superuser = true` → Solo administradores
- `can_view_dashboard = true` → Solo usuarios con dashboard
- `email LIKE '%@%'` → Solo usuarios con email
- `date_joined >= '2025-07-13'` → Usuarios creados hoy

---

## 📱 **EXPORTAR DATOS**

### **Desde pgAdmin4:**
1. **Seleccionar los datos** que quieres exportar
2. **Click derecho** → **"Copy"**
3. **Pegar en Excel o archivo de texto**

### **O usar consulta SQL:**
```sql
COPY (
    SELECT username, email, is_superuser, can_view_dashboard 
    FROM users_user
) TO '/tmp/usuarios.csv' WITH CSV HEADER;
```

---

## 🚨 **TROUBLESHOOTING**

### **Si no puedes conectar:**
1. **Verificar que PostgreSQL esté corriendo:**
   ```bash
   sudo systemctl status postgresql
   ```

2. **Verificar conexión:**
   ```bash
   psql -h localhost -U erp_user -d erp_dashboard_db -c "SELECT 1;"
   ```

3. **Verificar credenciales en .env:**
   ```
   DATABASE_USER=erp_user
   DATABASE_PASSWORD=erp_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

### **Si no ves la tabla users_user:**
- Verificar que estás en la base de datos correcta: `erp_dashboard_db`
- Expandir completamente el árbol de navegación
- Refrescar (F5) la vista

---

## 🎉 **¡YA PUEDES VER USUARIOS EN PGADMIN4!**

### **Pasos resumidos:**
1. **Abrir pgAdmin4**
2. **Conectar a:** `localhost:5432` con usuario `erp_user`
3. **Navegar a:** `erp_dashboard_db` → `Schemas` → `public` → `Tables` → `users_user`
4. **Ver datos:** Click derecho → "View/Edit Data" → "All Rows"

**🔗 Interfaz gráfica completa para gestionar tu base de datos PostgreSQL**

*Guía creada: $(date)*