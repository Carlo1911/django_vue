# -*- coding: utf-8 -*-
"""Fabfile de procedimientos de deployment.

En el presente fabfile se desarrolla una serie de procedimientos que automatizan
las actividades de deployment para el presente proyecto.
"""
import os
from importlib import import_module
from uuid import uuid4

from fabric.api import *
from fabric.api import run, settings, sudo, task
from fabric.colors import *
from fabric.context_managers import cd
from fabric.contrib.files import exists, upload_template

from ..config import (
    CONFIG_CONTEXT,
    CONFIG_FILES,
    DEPLOY_PATHS,
    DEPLOY_TASKS,
    EXCLUDED_FOLDERS,
    FTP_UPLOAD,
    GIT_URL,
    env,
)
from ..helpers import ConfigContext


@task
def update():
    role = env.roles[0]
    deploy_path = DEPLOY_PATHS[role]

    print('Update for {} begins.'.format(role))

    if role == 'staging':
        # Teardown: donde normalmente se limpia todo. Se observa la destrucción
        # del directorio anterior del proyecto.
        print('Performing teardown procedures...')
        if EXCLUDED_FOLDERS:
            temp_folder = '/tmp/%s' % uuid4().hex
            while exists(temp_folder, use_sudo=True):
                temp_folder = '/tmp/%s' % uuid4().hex
            run('mkdir -p %s' % temp_folder)
            with settings(warn_only=True):
                for folder in EXCLUDED_FOLDERS:
                    run('mkdir -p %s/%s' % (temp_folder, folder))
                    run('mv -f %s/%s/* %s/%s' % (deploy_path, folder, temp_folder, folder))

        with settings(warn_only=True):
            sudo('rm -rf %s' % deploy_path)

        # Setup: Las operaciones que normalmente se realizan al haberse limpiado
        # el entorno, en este caso, copia todo el proyecto a su ubicación final.
        print('Performing setup procedures...')
        run('mkdir -p %s' % deploy_path)
        run('cp -R %s/* %s' % (os.getcwd(), deploy_path))

        if EXCLUDED_FOLDERS:
            with settings(warn_only=True):
                for folder in EXCLUDED_FOLDERS:
                    run('mkdir -p %s/%s' % (deploy_path, folder))
                    run('mv -f %s/%s/* %s/%s' % (temp_folder, folder, deploy_path, folder))
                sudo('rm -rf %s' % temp_folder)

    else:
        with cd(deploy_path):
            # Extraído de chaman.sh
            run('git pull')


@task
def update_ftp():
    role = env.roles[0]

    print('Update for %s begins.' % role)

    run('ncftpput -R -v -u "%s" -p "%s" -P %d %s %s %s' %
        (FTP_UPLOAD['username'], FTP_UPLOAD['password'], FTP_UPLOAD['port'],
         FTP_UPLOAD['hostname'], FTP_UPLOAD['folder'], os.getcwd()))


@task
def reload_nginx():
    with settings(warn_only=True):
        sudo('service nginx reload')


@task
def update_config():
    role = env.roles[0]
    with cd(DEPLOY_PATHS[role]):
        for key, value in CONFIG_FILES.items():
            print('Updating %s...' % value[role]['template'])
            upload_template(value[role]['template'], value[role]['path'],
                            ConfigContext(CONFIG_CONTEXT[key]), use_sudo=True,
                            backup=False)
            if 'link' in value[role]:
                run('ln -s %s %s' % (value[role]['path'], value[role]['link']))
            if value[role]['path'].endswith('.sh'):
                run('chmod 777 %s' % value[role]['path'])


@task
def clone():
    run('git clone %s %s' % (GIT_URL, DEPLOY_PATHS[env.roles[0]]))
