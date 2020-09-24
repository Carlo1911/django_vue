from django.db import models


# City where employees live
class City(models.Model):
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


# Employee title
class Title(models.Model):
    title_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title_name

    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'


class Employee(models.Model):
    employee_name = models.CharField(max_length=255)
    employee_city = models.ForeignKey(City, related_name='employee_city', on_delete=models.CASCADE)
    employee_title = models.ForeignKey(Title, related_name='employee_title', on_delete=models.CASCADE)

    def __str__(self):
        return self.employee_name

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
