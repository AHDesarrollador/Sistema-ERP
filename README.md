# ERP Dashboard System

Sistema ERP completo con Django y Dashboard interactivo usando Plotly Dash.

## Características

### 🔷 Backend (Django + DRF)
- **Gestión de Usuarios**: Autenticación, perfiles, roles
- **Inventario**: Productos, categorías, proveedores, control de stock
- **Ventas**: Clientes, ventas, reportes automáticos
- **API RESTful**: Endpoints completos para todas las funcionalidades

### 🔷 Dashboard Interactivo
- **Visualizaciones en tiempo real** con Plotly Dash
- **Métricas de negocio**: Ventas, inventario, productos con bajo stock
- **Gráficos dinámicos**: Barras, pasteles, series temporales
- **Interfaz responsive** con Bootstrap

### 🔷 Base de Datos
- **PostgreSQL** configurado (fácilmente cambiable a SQLite para desarrollo)
- **Modelos relacionales** optimizados
- **Migraciones** automáticas

## Instalación y Configuración

### 1. Clona el proyecto
```bash
git clone https://github.com/AHDesarrollador/Sistema-ERP.git
cd erp_dashboard_project
```

### 2. Configura el entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno
Copia el archivo `.env` y ajusta los valores:
```bash
cp .env.example .env
```

Variables principales:
```
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_NAME=erp_dashboard_db
DATABASE_USER=postgres
DATABASE_PASSWORD=tu-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Configura PostgreSQL (Opcional)
Si usas PostgreSQL, crea la base de datos:
```sql
CREATE DATABASE erp_dashboard_db;
CREATE USER postgres WITH PASSWORD 'tu-password';
GRANT ALL PRIVILEGES ON DATABASE erp_dashboard_db TO postgres;
```

Para desarrollo rápido, puedes cambiar a SQLite editando `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 6. Ejecuta las migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crea un superusuario
```bash
python manage.py createsuperuser
```

### 8. Ejecuta el servidor
```bash
python manage.py runserver
```

## URLs Principales

- **Home**:http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/   (mailto:admin@erp.com/admin123)
- **API Root**: http://localhost:8000/api/
- **Dashboard**: http://localhost:8000/dashboard/ (mailto:admin@erp.com/admin123)
- **Docs**: http://localhost:8000/api/docs/






## API Endpoints

### Usuarios
- `POST /api/users/register/` - Registro de usuario
- `POST /api/users/login/` - Login
- `GET /api/users/profile/` - Perfil del usuario
- `GET /api/users/list/` - Lista de usuarios

### Inventario
- `GET/POST /api/inventory/products/` - Productos
- `GET/POST /api/inventory/categories/` - Categorías
- `GET/POST /api/inventory/suppliers/` - Proveedores
- `GET/POST /api/inventory/stock-movements/` - Movimientos de stock
- `GET /api/inventory/stats/` - Estadísticas de inventario

### Ventas
- `GET/POST /api/sales/sales/` - Ventas
- `GET/POST /api/sales/customers/` - Clientes
- `GET /api/sales/stats/` - Estadísticas de ventas
- `POST /api/sales/reports/generate/` - Generar reportes

## Uso del Dashboard

### 1. Obtén tu token de API
```bash
# Desde el shell de Django
python manage.py shell
```
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='tu-usuario')
token, created = Token.objects.get_or_create(user=user)
print(f"Tu token: {token.key}")
```

### 2. Accede al Dashboard
- Ve a http://localhost:8000/dashboard/
- Ingresa tu token de API
- Explora las métricas y gráficos interactivos

## Estructura del Proyecto

```
erp_dashboard_project/
├── manage.py
├── requirements.txt
├── .env
├── erp_dashboard_project/
│   ├── settings.py          # Configuración principal
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── apps/
│   ├── users/              # Gestión de usuarios
│   │   ├── models.py       # User, UserProfile
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   └── urls.py
│   ├── inventory/          # Gestión de inventario
│   │   ├── models.py       # Product, Category, Supplier, StockMovement
│   │   ├── views.py        # API views + stats
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── sales/              # Gestión de ventas
│   │   ├── models.py       # Sale, SaleItem, Customer, SaleReport
│   │   ├── views.py        # API views + reporting
│   │   ├── serializers.py
│   │   └── urls.py
│   └── dashboard/          # Dashboard interactivo
│       ├── dash_app.py     # Aplicación Dash
│       ├── views.py        # Vistas Django
│       ├── urls.py
│       └── templates/
└── media/                  # Archivos subidos
```

## Funcionalidades Implementadas

### ✅ Sistema de Usuarios
- Modelo de usuario personalizado
- Autenticación por token
- Perfiles de usuario
- Gestión de permisos

### ✅ Gestión de Inventario
- CRUD completo de productos
- Categorías y proveedores
- Control de stock automático
- Alertas de stock bajo
- Movimientos de inventario

### ✅ Sistema de Ventas
- Creación de ventas con múltiples items
- Gestión de clientes
- Cálculo automático de totales
- Reportes de ventas por período
- Estadísticas en tiempo real

### ✅ Dashboard Interactivo
- Métricas clave del negocio
- Gráficos interactivos
- Datos en tiempo real
- Interfaz responsive

## Próximos Pasos

### 🔧 Mejoras Técnicas
- [ ] Implementar cache con Redis
- [ ] Añadir tests automatizados
- [ ] Configurar CI/CD
- [ ] Optimizar consultas de base de datos
- [ ] Añadir logging avanzado

### 🎨 Mejoras de UI/UX
- [ ] Interfaz de administración personalizada
- [ ] Notificaciones en tiempo real
- [ ] Filtros avanzados en el dashboard
- [ ] Exportación de reportes (PDF, Excel)
- [ ] Dashboard móvil nativo

### 📊 Funcionalidades de Negocio
- [ ] Gestión de compras
- [ ] Control de calidad
- [ ] Integración con facturación
- [ ] Análisis predictivo
- [ ] Multi-tienda/sucursales

## Tecnologías Utilizadas

- **Backend**: Django 5.2, Django REST Framework
- **Base de Datos**: PostgreSQL (SQLite para desarrollo)
- **Dashboard**: Plotly Dash, Bootstrap
- **Frontend**: HTML, CSS, JavaScript
- **Autenticación**: Token-based
- **Visualizaciones**: Plotly, Pandas

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.