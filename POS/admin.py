from django.contrib import admin

from django.contrib.postgres import fields

from .models import *

# Register your models here.

admin.site.register(Item)
# admin.site.register(test)
admin.site.register(sellReceipt)
admin.site.register(buyReceipt)

'''
@admin.register(sellReceipt)
class sellReceiptAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
'''