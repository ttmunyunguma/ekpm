from django.contrib import admin
from .models import Organisation, Country, PropertyManager, User, LandLord, PropertyUnit, Property, Tenant


admin.site.register(User)
admin.site.register(PropertyManager)
admin.site.register(Country)
admin.site.register(Organisation)
admin.site.register(LandLord)
admin.site.register(Property)
admin.site.register(PropertyUnit)
admin.site.register(Tenant)
