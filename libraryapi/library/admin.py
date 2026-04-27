from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Document, DocumentAccess, Payment


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': ('avatar', 'role', 'is_verified_librarian')
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Document)
admin.site.register(DocumentAccess)
admin.site.register(Payment)