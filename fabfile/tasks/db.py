# -*- coding: utf-8 -*-

from fabric.api import run, task
from invoke import Responder

from ..config import *


def normalize_password(password):
    return password.replace('$', '\\$')


@task
def mysql_dropdb():
    role = env.roles[0]
    for data in DATABASES[role].values():
        run(
            'echo \'DROP DATABASE IF EXISTS %s;\' | mysql -u\'%s\' -p\'%s\''
            % (data['name'],
               data['username'],
               normalize_password(data['password']),),
            shell_escape=False
        )


@task
def mysql_createdb():
    role = env.roles[0]
    for data in DATABASES[role].values():
        run(
            'echo \'CREATE DATABASE %s;\' | mysql -u\'%s\' -p\'%s\''
            % (data['name'],
               data['username'],
               normalize_password(data['password'])),
            shell_escape=False
        )


@task
def mysql_loaddb(name='default'):
    role = env.roles[0]
    run(
        'mysql -u\'%s\' -p\'%s\' %s < %s/%s'
        % (DATABASES[role][name]['username'],
           normalize_password(DATABASES[role][name]['password']),
           DATABASES[role][name]['name'],
           DEPLOY_PATHS[role], DUMP_FILE),
        shell_escape=False
    )


@task
def mysql_dumpdbs():
    role = env.roles[0]
    for data in DATABASES[role].values():
        run(
            'mysqldump -u\'%s\' -p\'%s\' %s > %s/%s'
            % (data['username'],
               normalize_password(data['password']),
               data['name'],
               env['new_folder'],
               'dump_%s.sql' % data['name']
               ),
            shell_escape=False
        )


@task
def postgres_dropdb():
    role = env.roles[0]
    for data in DATABASES[role].values():
        run('psql -U {0} -h 127.0.0.1 -c "DROP DATABASE {1}"'.format(data['username'], data['name']))


@task
def postgres_createdb():
    role = env.roles[0]
    for data in DATABASES[role].values():
        run(
            'psql -U {0} -h 127.0.0.1 -c "CREATE DATABASE {1} WITH OWNER {2} ENCODING=\'UTF8\' TEMPLATE=template0"'.format(data['username'], data['name'], data['username']))


@task
def postgres_loaddb():
    role = env.roles[0]
    for data in DATABASES[role].values():
        run('psql -U {0} -h 127.0.0.1 -d {1} -f "{2}/{3}"'.format(data['username'], data['name'], data['dump_route'], data['file_name']))


@task
def postgres_dumpdbs():
    role = env.roles[0]
    for data in DATABASES[role].values():
        run('pg_dump -U {0} -h 127.0.0.1 -w {1} > {2}/{3}'.format(data['username'], data['name'], data['dump_route'], data['file_name']))
