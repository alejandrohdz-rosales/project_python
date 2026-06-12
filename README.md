# CRM SaaS B2B API

API REST desarrollada con Django y Django REST Framework para un sistema CRM SaaS B2B multi-tenant.

El proyecto permite a múltiples organizaciones gestionar sus usuarios y clientes de forma independiente mediante una arquitectura que garantiza el aislamiento de datos entre empresas.

## Características

* Arquitectura SaaS Multi-Tenant
* Autenticación JWT
* Gestión de organizaciones
* Gestión de usuarios
* Gestión de clientes
* Control de acceso basado en roles (RBAC)
* Sistema de permisos personalizados
* APIs REST escalables
* Validación y serialización de datos
* Control de versiones con Git

## Tecnologías

* Python
* Django
* Django REST Framework
* JWT Authentication
* PostgreSQL
* Git
* GitHub

## Arquitectura

Cada organización opera de forma independiente dentro de la plataforma. Los usuarios pertenecen a una organización específica y únicamente pueden acceder a los recursos autorizados según sus roles y permisos.

El sistema implementa:

* Aislamiento de datos por organización
* Control de acceso basado en roles
* Permisos a nivel de recurso
* Autenticación mediante tokens JWT

## Módulos

### Organizaciones

Permite crear y administrar organizaciones dentro de la plataforma.

Funciones principales:

* Crear organización
* Consultar organización
* Actualizar organización

### Usuarios

Gestión completa de usuarios asociados a una organización.

Funciones principales:

* Registro de usuarios
* Inicio de sesión
* Perfil del usuario autenticado
* Búsqueda por nombre
* Búsqueda por correo electrónico
* Actualización de usuarios

### Sales

Gestión de ventas pertenecientes a cada organización.

Funciones principales:

Crear ventas
Consultar ventas
Actualizar ventas
Eliminar ventas

### Roles y Permisos

Sistema de autorización diseñado para restringir el acceso a recursos según el rol asignado al usuario.

Ejemplos:

* Administrador
* Manager
* Usuario estándar

## Seguridad

* Autenticación JWT
* Validación de permisos
* Restricción de acceso por organización
* Protección de recursos sensibles
* Aislamiento de datos entre tenants

## Objetivos del Proyecto

Este proyecto fue desarrollado con fines de aprendizaje y práctica profesional para profundizar conocimientos en:

* Arquitectura Backend
* Desarrollo de APIs REST
* Multi-Tenancy
* Autenticación y Autorización
* Diseño de Software
* Buenas prácticas con Django y DRF

## Estado del Proyecto

En desarrollo activo.

Nuevas funcionalidades y mejoras continúan siendo implementadas.
