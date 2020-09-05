from django.contrib import admin
from app.core.models import User, Car, Model, Type, CarNumber


admin.site.register(User)
admin.site.register(Car)
admin.site.register(Model)
admin.site.register(Type)
admin.site.register(CarNumber)


@admin.register
class TripAdmin(admin.ModelAdmin):
    fields = (
        'id', 'pick_up_address', 'drop_off_address', 'status',
        'driver', 'rider',
        'created', 'updated',
    )
    list_display = (
        'id', 'pick_up_address', 'drop_off_address', 'status',
        'driver', 'rider',
        'created', 'updated',
    )
    list_filter = (
        'status',
    )
    readonly_fields = (
        'id', 'created', 'updated',
    )
