# -*- coding: utf-8 -*-

from fabric.api import *
from fabric.api import run, settings, task
from fabric.context_managers import cd

from ..config import *


def env_names(role):
    env_path = CONFIG_CONTEXT['virtualenv']['%s_env' % role].split('/')
    folder = '/'.join(env_path[:-1])
    name = env_path[-1]
    return folder, name


@task
def virtualenv():
    folder, name = env_names(env.roles[0])
    with cd(folder):
        run('virtualenv -p python3 %s' % name)


@task
def requirements():
    folder, name = env_names(env.roles[0])
    run('%s/%s/bin/pip install -r %s/%s' %
        (folder, name, CLONE_PATH[env.roles[0]], REQUIREMENTS_FILE,))


@task
def migrate():
    folder, name = env_names(env.roles[0])
    settings_ = ''
    if env.roles[0] == 'staging':
        settings_ = '_staging'
    with cd(DEPLOY_PATHS[env.roles[0]]):
        run('%s/%s/bin/python3 backend/manage.py migrate '
            '--settings=config.settings%s --noinput' % (folder, name, settings_))


@task
def start_supervisord():
    folder, name = env_names(env.roles[0])
    with settings(warn_only=True):
        with cd(DEPLOY_PATHS[env.roles[0]]):
            run('supervisord -c %s' %
                (CONFIG_FILES['supervisord'][env.roles[0]]['path'],))


@task
def stop_supervisord():
    folder, name = env_names(env.roles[0])
    with settings(warn_only=True):
        with cd(DEPLOY_PATHS[env.roles[0]]):
            run('supervisorctl -c %s stop all' %
                (CONFIG_FILES['supervisord'][env.roles[0]]['path'],))


@task
def custom():
    folder, name = env_names(env.roles[0])
    settings_ = ''
    if env.roles[0] == 'staging':
        settings_ = '_staging'
    with cd(DEPLOY_PATHS[env.roles[0]]):
        run('%s/%s/bin/python3 backend/manage.py %s '
            '--settings=config.settings%s' %
            (folder, name, CUSTOM_COMMAND, settings_))
