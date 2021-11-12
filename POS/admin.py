from django.contrib import admin

from django.contrib.postgres import fields

from .models import Item, sellReceipt

# Register your models here.

admin.site.register(Item)
# admin.site.register(test)
admin.site.register(sellReceipt)

'''
@admin.register(sellReceipt)
class sellReceiptAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
'''