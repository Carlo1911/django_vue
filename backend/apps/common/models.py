# -*- coding: utf-8 -*-
"""
Utilidades para Modelos
=======================
"""
from django.db import models
from model_utils.models import TimeStampedModel


class FakeCharField(str):
    """
    Clase que finge ser un CharField sin tener efecto en la base de datos. Se
    puede utilizar para tareas que requieran simular la existencia de un campo
    temporal sin afectar el modelo de datos original.
    """

    def __new__(cls, value=None, short_description=None):
        self = super(FakeCharField, cls).__new__(cls, value)
        self.short_description = short_description
        return self


class BadWord(models.Model):
    """
    BadWord()

    Modelo simple que representa a una palabra a filtrar.

    :param word: Palabra a filtrar.
    :type word: CharField
    """

    word = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )


class CommonModel(TimeStampedModel):
    """
    Clase abstracta que registra estado, creación y modificación de las clases
    """
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if getattr(self, 'name', None):
            return self.name
        else:
            return super(CommonModel, self).__str__()

    class Meta:
        abstract = True
