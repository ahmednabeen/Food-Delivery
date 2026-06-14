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
    list_display = ('id', 'name', 'address', 'phone', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'address', 'phone', 'email')
    list_editable = ('status',)
    list_per_page = 20
    ordering = ('-created_at',)

    actions = ['mark_preparing', 'mark_out_for_delivery', 'mark_delivered']

    def mark_preparing(self, request, queryset):
        updated = queryset.update(status='Preparing')
        self.message_user(request, f'{updated} order(s) marked as Preparing.')
    mark_preparing.short_description = 'Mark selected orders as Preparing'

    def mark_out_for_delivery(self, request, queryset):
        updated = queryset.update(status='Out for Delivery')
        self.message_user(request, f'{updated} order(s) marked as Out for Delivery.')
    mark_out_for_delivery.short_description = 'Mark selected orders as Out for Delivery'

    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='Delivered')
        self.message_user(request, f'{updated} order(s) marked as Delivered.')
    mark_delivered.short_description = 'Mark selected orders as Delivered'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
