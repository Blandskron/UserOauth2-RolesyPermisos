# Proyecto: Sistema de Roles y Permisos en Django

## Descripción

Este proyecto es una aplicación desarrollada en Django que implementa un sistema de autenticación, gestión de usuarios, roles y permisos, permitiendo un control detallado sobre el acceso a los documentos según los permisos asignados a cada usuario.

La aplicación cuenta con una estructura modular que incluye:

- **Autenticación de usuarios:** Login, logout y registro.
- **Control de permisos y roles:** Mediante grupos y permisos de Django.
- **Gestión de documentos:** Acceso restringido a los documentos según el usuario y su grupo.
- **Frontend básico en Django:** Para la interacción con el sistema.

## Tecnologías utilizadas

- Django
- Django ORM
- SQLite / PostgreSQL (según configuración)
- HTML, CSS (para la interfaz básica)

## Estructura del Proyecto

```
backend/
├── core/
│   ├── models.py       # Definición de modelos de usuarios y documentos
│   ├── views.py        # Vistas para autenticación y documentos
│   ├── urls.py         # Rutas de la aplicación
│   ├── admin.py        # Registro de modelos en el panel de administración
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── document_list.html
│   ├── ...
├── manage.py
├── db.sqlite3 (o configuración para PostgreSQL)
```

## Instalación y Configuración

1. Clonar el repositorio:
   ```bash
   git clone <repositorio>
   cd backend
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```
5. Crear un superusuario:
   ```bash
   python manage.py createsuperuser
   ```
6. Ejecutar el servidor:
   ```bash
   python manage.py runserver
   ```

## Gestión de Roles y Permisos

- Se han definido tres grupos de usuarios:
  - **Admin:** Acceso completo (crear, editar y eliminar documentos).
  - **Editor:** Puede crear y editar documentos.
  - **Viewer:** Solo puede ver documentos.
- Los permisos se gestionan a través del panel de administración de Django (`/admin`).

## Acceso a la Aplicación

- **Login:** `/login/`
- **Logout:** `/logout/`
- **Registro:** `/register/`
- **Lista de Documentos:** `/documents/`

## Futuras Mejoras

- Implementación de un sistema de notificación.
- Integración con API REST para mejorar la interoperabilidad.
- Interfaz más avanzada con React o Vue.js.

---

Este proyecto demuestra cómo utilizar Django para la gestión segura de roles y permisos, asegurando que cada usuario acceda solo a la información que le corresponde.
