# -*- coding: utf-8 -*-

from fabric.api import env

# La lista de tareas a ejecutarse en cada 'deploy'. Comentar y descomentar según
# sea necesario. Si se creas nuevas tareas, añádelas aquí.

# Si borran alguna de estas entradas tanto en este archivo como en el directorio
# de tareas, HAY TABLA

DEPLOY_TASKS = [
    # 'sys.install_dependencies',
    # 'db.postgres_dumpdbs',
    # 'db.postgres_dropdb',
    # 'db.postgres_createdb',
    # 'db.postgres_loaddb',
    # 'deploy.clone',
    # 'django.virtualenv',
    'django.requirements',
    'django.stop_supervisord',
    'deploy.update',
    # 'deploy.update_ftp',
    'django.migrate',
    # 'django.custom',
    'deploy.update_config',
    'deploy.reload_nginx',
    'django.start_supervisord',
]

CUSTOM_COMMAND = ''


# Definimos algunos datos sobre los servidores y con qué identidad ejecutaremos
# los comandos.
env.roledefs = {
    'staging': ['jenkins@172.16.4.105'],
    'production': ['jenkins@jenkins.phantasia.pe']
}

# Se definen las contraseñas para cada uno de los usuarios de los servidores
# que vayamos a utilizar. Notar que es necesario poner el número de puerto
# (normalmente 22) para cada entrada de esta lista.
env.passwords = {
    'jenkins@172.16.4.105:22': 'K%Iq3yzRDsEtN:8{n1Hf',
    'root@production:22': 'j3nk1s**111'
}


# Las rutas donde se ubicarán los archivos del proyecto (no necesariamente es
# donde se clonará el repositorio, ver más abajo.
DEPLOY_PATHS = {
    'staging': '/var/www/nginx/2019/backend/skeleton',
    'production': '/var/www/nginx/2019/backend/skeleton',
}

# La ruta donde se ubicará el repositorio git del proyecto, no necesariamente
# es la carpeta del deployment
CLONE_PATH = {
    'staging': '/var/lib/jenkins/workspace/backend_skeleton',
    'production': '/var/lib/jenkins/workspace/demo'
}

# El URL de donde se clonará el proyecto
GIT_URL = 'git@bitbucket.org:wunderman-phantasia/backend_skeleton.git'

# Con cada nuevo update se realiza un backup de la base de datos para tener
# respaldos. Cambiar esta variable a False desactivará los backups. Usar cuando
# no se requiera el uso de bases de datos.
CREATE_DUMP = False

# Sólo para uso avanzado: La tarea que realiza el dump de las BD entre
# versiones.
DUMP_TASK = 'postgres_dumpdbs'

# Si se desea que script ingrese a la base de datos y cree una base de datos
# nueva (o la limpie si existe), rellenar los datos de acceso y el nombre de la
# DB.
DATABASES = {
    'staging': {
        'default': {
            'name': 'db_backend',
            'username': 'postgres',
            'password': '3ZVTwkVc9negLbmq',
            'host': '127.0.0.1',
            'dump_route': '/var/www/nginx/2019/backend/skeleton',
            'file_name': 'dump_db_backend.sql',
        }
    },

    'production': {
        'default': {
            'name': '',
            'username': '',
            'password': '',
            'host': '127.0.0.1',
        }
    }
}

# Si se usa la tarea de actualización por ftp, se debe declarar la información
# necesaria para la conexión al servidor remoto.
FTP_UPLOAD = {
    'hostname': 'localhost',
    'username': 'anonymous',
    'password': '',
    'port': 21,
    'folder': '/'
}

# Definición de los ficheros de configuración. Se necesitan definir los ámbitos
# de staging y production siempre. Se especifica la ruta de cada plantilla y su
# ubicación final en el sistema.
#
# Pueden crearse cuantas entradas sean necesarias siempre y cuando exista un
# contexto para ellas (ver abajo) y tengan un formato válido (ver nginx.conf)
# para una referencia sobre la sintaxis de las variables.
CONFIG_FILES = {
    'nginx': {
        'staging': {
            'template': 'deploy/nginx.staging.conf',
            'path': '/etc/nginx/conf.d/backend-staging.phantasia.pe.conf'
        },

        'production': {
            'template': 'deploy/nginx_static.conf',
            'path': '/etc/nginx/sites-available/.conf',
            'link': '/etc/nginx/sites-enabled/.conf'
        }
    },

    # Usar sólo con rails/django
    'supervisord': {
        'staging': {
            'template': 'deploy/supervisord.staging.conf',
            'path': 'backend/supervisord.staging.conf'
        },

        'production': {
            'template': 'deploy/supervisord.conf',
            'path': 'backend/supervisord.conf'
        }
    },

    'gunicorn': {
        'staging': {
            'template': 'deploy/gunicorn_start.staging.sh',
            'path': 'backend/gunicorn_start.staging.sh'
        },

        'production': {
            'template': 'deploy/gunicorn_start.sh',
            'path': 'backend/gunicorn_start.sh'
        }
    }
}


# El contexto es un conjunto de variables que estarán presentes para cada
# template definido en la sección anterior. Nótese que cada entrada de este
# setting debe coincidir con la del setting anterior
CONFIG_CONTEXT = {
    'nginx': {
        'staging_server_name': 'backend-staging.phantasia.pe',
        'production_server_name': 'backend-staging.phantasia.pe',

        # Usar sólo con archivos estáticos o proyectos de PHP
        # 'staging_root': '/var/www/nginx/2017/',
        # 'production_root': '/var/www/nginx/2014/demo/demo-staging',

        # Usar sólo con rails/django
        'upstream_name': 'backend',
        'upstream_socket': '/tmp/backend.sock',

        'staging_rootfiles': '/var/www/nginx/2019/backend/skeleton/',
        'production_rootfiles': '/var/www/nginx/2019/backend/skeleton/',

        'staging_staticfiles': '/var/www/nginx/2019/backend/skeleton/backend/static',
        'production_staticfiles': '/var/www/nginx/2019/backend/skeleton/backend/static',

        'staging_mediafiles': '/var/www/nginx/2019/backend/skeleton/backend/media/',
        'production_mediafiles': '/var/www/nginx/2019/backend/skeleton/backend/media'
    },

    # Usar sólo con django
    'supervisord': {
        'staging_user': 'jenkins',
        'production_user': '',
        'program_name': 'backend_2019',
        'staging_working_dir': '/var/www/nginx/2019/backend/skeleton',
        'production_working_dir': '',
        'staging_wsgi_file': 'wsgi_staging',
        'staging_env': '/var/lib/jenkins/backend-env',
        'production_wsgi_file': 'wsgi',
    },

    'virtualenv': {
        'staging_env': '/var/lib/jenkins/backend-env',
        'production_env': '/var/lib/jenkins/backend-env'
    },

    'gunicorn': {
        'instance_name': 'backend',
        'workers': 4,
        'staging_env': '/var/lib/jenkins/backend-env',
        'production_env': '/var/lib/jenkins/backend-env',
        'upstream_socket': '/tmp/backend.sock',
    }
}

# Si se necesitase restaurar una base de datos a partir de un archivo, definir
# su ruta en esta variable.
DUMP_FILE = 'db/script.sql'

# Durante el proceso de actualización se limpian todos los folders
# pertenecientes al proyecto, si se desea evitar este comportamiento para
# algunos de ellos, colocar sus rutas aquí.
EXCLUDED_FOLDERS = []

# Sólo django: La ruta hacia el archivo de los requerimientos.
REQUIREMENTS_FILE = 'backend/requirements.pip'

# La lista de dependencias del sistema a instalar (usando apt-get)
SYSTEM_DEPENDENCIES = ['python-pip', 'git', 'build-essential']
