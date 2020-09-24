from django.contrib import admin
from company.models import City, Title, Employee


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fields = ('city_name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    fields = ('title_name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ('employee_name', 'employee_city', 'employee_title',)
