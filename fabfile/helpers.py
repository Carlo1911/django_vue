# -*- coding: utf-8 -*-


class ConfigContext(dict):
    """
    Clase de ayuda para la configuración, permite acceder a los valores de un
    diccionario con la notación:

    dic.clave -> valor
    """

    def __getattr__(self, item):
        item_ = self.__getitem__(item)
        if type(item_) == dict:
            return ConfigContext(item_)
        return item_
