# -*- coding: utf-8 -*-
from importlib import import_module
import tasks
from fabric.api import *

from .config import DEPLOY_TASKS


@task(default=True)
def deploy():
    for task_ in DEPLOY_TASKS:
        task_module, task_name = task_.split('.')
        module = import_module('.tasks.%s' % task_module, 'fabfile')
        executable_task = getattr(module, task_name)
        execute(executable_task)
