from django.contrib import admin

from .models import Location, Category


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
