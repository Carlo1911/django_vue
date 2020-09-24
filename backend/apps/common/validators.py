# -*- coding: utf-8 -*-
"""
Validadores de entrada
======================

name_validator: Valida la presencia de caracteres alfabéticos y especiales adecuados para un
nombre.

dni_validator: Valida la presencia de 8 caracteres numéricos.

phone_validator: Valida la presencia de 7 a 14 caracteres numéricos con espacios y guiones (``-``).

alphanumeric_validator: Valida la presencia de todos los caracteres imprimibles incluyendo aquellos usados en el idioma castellano.
"""
import os
import re
from functools import reduce

from common.models import BadWord
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import RegexValidator
from django.db.models import Q
from django.utils.deconstruct import deconstructible

name_validator = RegexValidator(r'^[a-zA-z \-\'áéíóúÁÉÍÓÚñÑüÜïÏöÖ]+$')

dni_validator = RegexValidator(r'^[0-9]{8}$')

phone_validator = RegexValidator(r'^\+?[0-9 -]{7,14}$')

alphanumeric_validator = RegexValidator(r'^[ -~áéíóúÁÉÍÓÚñÑüÜ¡¿]+$')


@deconstructible
class ImageSize(object):
    """
    Clase que valida el tamaño de una imagen
    """

    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

    def __call__(self, value):
        img_width, img_height = get_image_dimensions(value)
        errors = []
        if self.width is not None and img_width != self.width:
            errors.append('El ancho debe ser {} px.'.format(self.width))
        if self.height is not None and img_height != self.height:
            errors.append('La altura debe ser {} px.'.format(self.height))
        raise ValidationError(errors)


@deconstructible
class FileExtensionValidator(object):
    """
    Clase que valida la extensión de un archivo en
    base a una lista de permitidos

    :param extensions: La cadena que se validará.
    :type extensions: list
    """

    def __init__(self, extensions=None,):
        self.extensions = extensions

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in self.extensions:
            raise ValidationError('Seleccione un archivo soportado.')


@deconstructible
class ImgSize(object):

    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

    def __call__(self, value):
        img_width, img_height = get_image_dimensions(value)
        errors = []
        if self.width is not None and img_width != self.width:
            errors.append('El ancho debe ser {} px.'.format(self.width))
        if self.height is not None and img_height != self.height:
            errors.append('La altura debe ser {} px.'.format(self.height))
        raise ValidationError(errors)


def is_bad_word(text):
    """
    Función para determinar la validez de un texto contra la lista de palabras
    existentes en la base de datos.

    :param text: La cadena que se validará.
    :type text: str o unicode
    :return: Un booleano representando la validez del texto.
    :rtype: bool
    """

    text = text.strip()
    text = re.sub(r'\s+', u' ', text)
    rules = [
        (r'1', u'i'),
        (r'2', u'dos'),
        (r'3', u'e'),
        (r'4', u'a'),
        (r'5', u's'),
        (r'6', u'g'),
        (r'7', u't'),
        (r'8', u'b'),
        (r'9', u'g'),
        (r'0', u'o'),
        (r'[^\w\s]+', u'')
    ]

    validation_text = text[:]

    for pattern, replace in rules:
        validation_text = re.sub(pattern, replace, validation_text,
                                 flags=re.UNICODE)

    initial_validation = Q(word__iexact=validation_text)
    validation_text = validation_text.split(' ')
    validation_text = [Q(word__iexact=t) for t in validation_text]
    validation_text.append(initial_validation)
    query = reduce(lambda x, y: x | y, validation_text)
    return BadWord.objects.filter(query).exists()
