# -*- coding: utf-8 -*-
import os

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from unipath import Path


class Command(BaseCommand):

    """
    Cargar fixtures del proyecto.
    """

    _files_ignored = 'test'
    _message_finish = 'Successfully populated'

    _fixtures_order = [
        'users',
        'ubigeo',
    ]

    help = 'Cargar fixtures del proyecto'

    def _get_list_files(self, path):
        """
        Dada un directorio, retornar lista de archivos que tiene.
        """

        list_files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            filenames = [f for f in filenames if self._files_ignored not in f]
            if not filenames:
                continue
            list_files.extend(filenames)
        return list_files

    def get_fixture_paths(self):
        """
        Obtiene una lista de archivos fixtures dentro del directorio fixtures.
        """

        fixtures = []
        for app_path in [a.path for a in apps.get_app_configs()]:
            fixture_path = os.path.join(app_path, 'fixtures')
            if os.path.exists(fixture_path):
                fixtures.extend(self._get_list_files(fixture_path))
        return fixtures

    def _order_fixtures(self, fixtures):
        response = list()
        for fixture in self._fixtures_order:
            for value in fixtures:
                filename = str(Path(value).stem)
                if fixture == filename:
                    response.append(value)
                    break
        return response

    def handle(self, *args, **options):
        # Populating fixtures
        fixtures = self.get_fixture_paths()
        fixtures = self._order_fixtures(fixtures)
        for fixture in fixtures:
            call_command(
                'loaddata',
                fixture,
                verbosity=1,
            )
        # Registering triggers
        # call_command(
        #     'audit_schema',
        #     verbosity=1,
        # )
        self.stdout.write(self._message_finish)
