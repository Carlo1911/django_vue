# Esqueleto de Django para proyectos de Wunderman Thompson

Este esqueleto debe usarse para TODOS los proyectos que usen Django.
Una vez descargado, se debe:

* Instalar Docker en la pc de desarrollo: https://docs.docker.com/install/
* Eliminar la carpeta `.git` y comenzar un proyecto nuevo en un repositorio distinto. **ESTO ES MUY IMPORTANTE. POR FAVOR NO OLVIDAR ESTE PASO.**
* Crear un entorno virtual e instalar los requerimientos del proyecto: ```pip install -r project_requirements.pip```
* Para activar pre-commit: ```pre-commit install-hooks```
* Crear un archivo .env a partir de .env.example y configurar los datos del proyecto.
* Dentro del directorio ejecutar: `make build` para crear la imagen del proyecto.
* Dentro del directorio ejecutar: `make up` para levantar el proyecto.
* Dentro de /frontend ejecutar: `npm install` para cargar los archivos de front.
* Editar `config/settings.py`, `config/settings_staging.py` convenientemente. Recordar el cambiar la variable `SECRET_KEY` con un valor completamente aleatorio.
---
### Comandos adicionales

* Aplicar cambios de template de Vue.js: ```./node_modules/.bin/webpack```
* Levantar el proyecto con los contenedores respectivos: `make up`
* Levantar el proyecto con los contenedores respectivos en un proceso de fondo: `make up-daemon`
* Crear la imagen del proyecto: `make build`
* Iniciar contenedores ya generados (builded): `make start`
* Detener contenedores: `make stop`
* Agregar archivos estáticos a la carpeta estática: `make collectstatic`
* Crear super usuario: `make superuser`
* Crear archivos de migración: `make migrations`
* Correr pruebas unitarias: `make test`
* Aplicar migraciones: `make migrate`
* Cargar data inicial (previa configuración en populate.py): `make loaddata`
* Ingresar a consola de Django: `make django-shell`
* Reiniciar contenedores: `make restart`
* Acceder al contenedor del proyecto: `make shell-web`
* Acceder al contenedor de postgresql: `make shell-db`
* Acceder al contenedor de nginx: `make shell-nginx`
* Acceder al log del contenedor del proyecto: `make log-web`
* Acceder al log del contenedor de postgresql: `make log-db`
* Acceder al log del contenedor de nginx: `make log-nginx`
---
## Estructura del esqueleto

  * Se debe mantener todo el código dentro de la carpeta `apps`, y distribuirlo convenientemente a través de *apps* (como `common`, y `website`).
  * Las *apps* no necesitan tener archivos obligatorios. No dejar archivos/carpetas vacías o inútiles.
  * Toda la configuración y archivos de inicialización del proyecto deben estar dentro de la carpeta `config`.
  * Se ha considerado el uso de Vue.js como framework base para el frontend de las páginas.
  * Para acceder a la página principal: http://localhost
  * Para acceder al administrador de Django: http://localhost/admin
  * Se tiene acceso a pgadmin4 a través de la ruta: http://localhost:5050
  * Se tiene acceso a flower a través de la ruta http://localhost:8888
---
## Documentación

  * Leer la documentación ubicada en `docs/build/html/index.html`
  * Si se desea incluir más documentación o nuevos módulos, añadirlos a `docs/source/common/index.rst` y ejecutar (dentro de la carpeta `docs`): `make html`
---
## Referencias

Base creada en base a:
- Deploy Django, Gunicorn, NGINX, Postgresql using Docker: [link](https://ruddra.com/docker-django-nginx-postgres/)
- Serve Static Files by Nginx from Django using Docker: [link](https://ruddra.com/serve-static-files-by-nginx-from-django-using-docker/)
- Docker: Use Celery in Django(Redis as Broker): [link](https://ruddra.com/docker-do-stuff-using-celery-using-redis-as-broker/)
