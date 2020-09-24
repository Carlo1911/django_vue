# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

path = str(Path(__file__).parent.parent.absolute())

if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_staging')

application = get_wsgi_application()
