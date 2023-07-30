from django.contrib import admin
from .models import Item, Category, Tag, Manufacturer, Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(Item, MarkdownxModelAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}

admin.site.register(Category, CategoryAdmin)

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}

admin.site.register(Manufacturer, ManufacturerAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}

admin.site.register(Tag, TagAdmin)

admin.site.register(Comment)


