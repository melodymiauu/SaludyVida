from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('correo', 'nombre', 'is_active', 'is_staff')
    search_fields = ('correo', 'nombre')
    ordering = ('correo',) 

    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Informacion personal', {'fields': ('nombre',)}), 
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'password', 'password2'),
        }),
    )