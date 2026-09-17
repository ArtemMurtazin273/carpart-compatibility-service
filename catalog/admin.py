from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from catalog.models import (
    Mechanic,
    Part,
    Manufacturer,
    PartCategory,
    Car,
)


@admin.register(Mechanic)
class MechanicAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("license_number",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("license_number",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "license_number",
                )
            },
        ),
    )


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("name", "part_number", "price", "manufacturer", "category")
    list_filter = ("category", "manufacturer")
    search_fields = ("name", "part_number")


admin.site.register(Manufacturer)
admin.site.register(PartCategory)
admin.site.register(Car)
