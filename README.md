# Proof of Concept: Arquitectura Multi-tenant Escalable (Python/Django & PostgreSQL)

## Propósito
Demostrar una solución robusta para servir múltiples clientes desde una única instancia de infraestructura, con aislamiento de datos por esquema en PostgreSQL usando Django y `django-tenants`. Contenerizado con Docker Compose y listo para portar a Kubernetes.

## Decisión Arquitectónica
Elegimos el modelo Schema-based Multi-tenancy con `django-tenants` para garantizar separación lógica estricta de datos por cliente (un esquema por tenant) optimizando recursos y facilitando el despliegue en contenedores. Esta arquitectura es ideal para entornos DataOps, permite migraciones por tenant y simplifica backups/restore selectivos.

## Tecnologías
- Python 3.11, Django 4.2
- PostgreSQL 15
- django-tenants
- Dockerfile + Docker Compose (lista para traducirse a Kubernetes)

## Cómo Ejecutar (DevOps)
1. Copia las variables:
   ```bash
   cp .env.example .env
   ```
2. Levanta los servicios:
   ```bash
   docker compose up --build
   ```
3. Crea tenants (usando dominios que resuelven a 127.0.0.1 vía localtest.me):
   ```bash
   docker compose exec web python manage.py provision_tenant --schema=clinic_a --domain=clinic-a.localtest.me
   docker compose exec web python manage.py provision_tenant --schema=clinic_b --domain=clinic-b.localtest.me
   ```

4. Prueba aislamiento (opcional): entra al shell del tenant y crea datos por separado.

## Notas para Kubernetes
Esta configuración está lista para ser traducida a un despliegue de Kubernetes con volúmenes persistentes y Services sin cambios en la app (solo manifests). Kubernetes leerá los Dockerfiles y definiciones de contenedor.
