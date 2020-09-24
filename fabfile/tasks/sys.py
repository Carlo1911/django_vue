# -*- coding: utf-8 -*-

from fabric.api import sudo, task

from ..config import SYSTEM_DEPENDENCIES


@task
def install_dependencies():
    sudo('apt-get install %s' % ' '.join(SYSTEM_DEPENDENCIES))
    sudo('pip install virtualenv')
