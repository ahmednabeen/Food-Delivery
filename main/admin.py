from django.contrib import admin
from django.utils.html import format_html
from .models import Food, BlogPost


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'display_price', 'star_display', 'time', 'image_preview')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image', 'price', 'category')
        }),
        ('Details', {
            'fields': ('time', 'rating', 'description')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'

    def star_display(self, obj):
        return obj.star_rating()
    star_display.short_description = 'Rating'


from .models import Order as OrderModel

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'address', 'phone', 'email')
    list_editable = ('status',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
