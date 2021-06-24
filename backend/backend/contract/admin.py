from django.contrib import admin

from .models import SmartContract, Contract

admin.site.register(SmartContract)
admin.site.register(Contract)