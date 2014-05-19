from django.contrib import admin
from Supermarket.models import *

class ItemInline(admin.TabularInline):
    model = Item
    extra = 2

class SimilarItemAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

admin.site.register(SalesClerk)
admin.site.register(Employee)
admin.site.register(Manager)
admin.site.register(Record)
admin.site.register(SimilarItem, SimilarItemAdmin)