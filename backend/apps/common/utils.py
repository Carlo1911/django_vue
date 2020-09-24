# -*- coding: utf-8 -*-
"""
Utilidades Varias
=================
"""

import datetime
import random
import sys
import unicodedata

import xlwt
from django.contrib import admin
from django.http import HttpResponse


class Numbers:
    """
    Clase de utilidades para trabajar con datos de tipo numérico.
    """

    @staticmethod
    def is_number(s):
        """
        Comprueba que un dato es del tipo numérico o contiene números.

        :param s: Dato que será comprobado.
        :return: ``True`` si ``s`` es numérico, ``False`` de otra forma.

        Uso:

        .. code:: python

            Numbers.is_number('123')  # True
            Numbers.is_number('uno')  # False
            Numbers.is_number(123)    # True
        """

        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


class RandomUtil:
    """
    Clase de utilidades para trabajar con elementos aleatorios.
    """

    max = sys.maxsize
    min = -sys.maxsize - 1

    @staticmethod
    def get_random_probability():
        """
        TODO: Llenar

        :return: None
        """
        systemRandom = random.SystemRandom()
        return systemRandom.random()

    @staticmethod
    def get_random_float(start=min, stop=max, decimal=2):
        """
        TODO: Llenar

        :param option_probability_dict: To be implemented
        :return: None
        """
        systemRandom = random.SystemRandom()
        random_number = systemRandom.uniform(start, stop)
        return round(random_number, decimal)

    @staticmethod
    def get_random_integer(start=min, stop=max, decimal=2):
        """
        TODO: Llenar

        :param option_probability_dict: To be implemented
        :return: None
        """
        systemRandom = random.SystemRandom()
        random_number = systemRandom.randrange(start, stop)
        return random_number

    @staticmethod
    def get_random_choice(list):
        """
        TODO: Llenar

        :param option_probability_dict: To be implemented
        :return: None
        """
        if list:
            systemRandom = random.SystemRandom()
            random_number = systemRandom.choice(list)
            return random_number

    @staticmethod
    def get_random_sample(list, list_length):
        """
        TODO: Llenar

        :param option_probability_dict: To be implemented
        :return: None
        """
        if list:
            systemRandom = random.SystemRandom()
            random_list = systemRandom.sample(list, 3)
            return random_list


def custom_titled_filter(title):
    """ Función que permite cambiar el nombre de un campo
    en el filtro para el administrador

    list_filter = (('created_date', custom_titled_filter('Fecha creación')),)
    """
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class ExportExcelMixin:
    """ Mixin que permite exportar los campos de un modelos en un archivo excel desde las
    acciones del admin
    Se debe heredar en la clase correspondiente y agregar:
    actions = ['export_xls']
    excel_columns = {
        'names': 'Nombres',
    }
    excel_columns_values = {
        'status': {True: 'Suscrito', False: 'No suscrito'}
    }
    """

    def export_xls(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')

        meta = self.model._meta

        response['Content-Disposition'] = 'attachment; filename={}.xls'.format(meta.model_name)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(meta.model_name)

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for ind, col_name in enumerate(self.excel_columns):
            ws.write(row_num, ind, self.excel_columns[col_name], font_style)

        def process_rows(obj):
            rows = []
            for field in self.excel_columns:
                if isinstance(getattr(obj, field), datetime.datetime):
                    row = getattr(obj, field).strftime('%d-%m-%Y %H:%M')
                elif field in self.excel_columns_values:
                    row = self.excel_columns_values[field][getattr(obj, field)]
                else:
                    row = getattr(obj, field)
                rows.append(row)
            return rows

        font_style = xlwt.XFStyle()
        for obj in queryset:
            row_num += 1
            rows = process_rows(obj)
            for col_num in range(len(rows)):
                ws.write(row_num, col_num, rows[col_num], font_style)
        wb.save(response)
        return response

    export_xls.short_description = 'Exportar Selección'
