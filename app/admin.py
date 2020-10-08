from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Category, Product, Lookbook, Look, VariationManager


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'parent', 'menu']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Lookbook)
class LookbookAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    list_display = ['image', 'category', 'slug']
    prepopulated_fields = {'slug': ('image',)}

# @admin.register(ProductSize)
# class ProductSizeAdmin(admin.ModelAdmin):
#     list_display = ['product', 'size',]
#     prepopulated_fields = {'size': ('size',)}





# @admin.register(VariationManager)
# class VariationManagerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_show', 'price', 'available', 'status', 'created', 'uploaded']
    list_filter = ['available', 'created', 'status', 'uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}


    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='70' />".format(obj.image.url))
        return "None"

    image_show.__name__="Картинка"


# class SizeAdmin(admin.ModelAdmin):
#     list_display = ['name','code']
#
#
# class VariantsAdmin(admin.ModelAdmin):
#     list_display = ['title','product','color','size','price','quantity','image_tag']
#
#
#
# admin.site.register(Size,SizeAdmin)










# class CategoryAdmin(admin.ModelAdmin):
#     list_select_related = ['parent']
#     list_display = ['name', 'parent', 'slug']
#     prepopulated_fields = {'slug': ('name', 'parent')}
# admin.site.register(Category, CategoryAdmin)
#
#
#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id','name', 'slug', 'price', 'stock', 'available', 'created', 'updated',]
#     # list_filter = ['available', 'created', 'updated']
#     list_editable = ['price', 'stock', 'available']
#     list_fields = ['s_size', 'm_size', 'l_size']
#     prepopulated_fields = {'slug': ('name',)}
# admin.site.register(Product, ProductAdmin)
