from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin, Group


# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('phone',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    search_fields = ('user_name', 'email')
    ordering = ('user_name',)
    list_display = ('user_name', 'email')

    # list_filter = ()

    readonly_fields = ('last_login',)

    fieldsets = (
        (None, {
            'fields': ('user_name', 'email', 'password', 'last_login')}
         ),
        ("Права", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")}
         ),

    )
    add_fieldsets = (
        (None, {
            'fields': ('user_name', 'email', 'password1', 'password2', 'last_login')}
         ),
        ("Права", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")}
         ),

    )
