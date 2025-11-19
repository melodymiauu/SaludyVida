from django.contrib import admin
from .models import Medico, Paciente, Cita

# Register your models here.
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_completo", "rut", "especialidad", "correo", "telefono")
    list_filter = ("nombre_completo", "especialidad")
    search_fields = ("nombre_completo", "especialidad", "rut")

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_completo", "rut", "fecha_nacimiento", "sexo", "telefono")
    list_filter = ("nombre_completo", "sexo", "fecha_nacimiento")
    search_fields = ("nombre_completo", "rut", "fecha_nacimiento")

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "medico", "especialidad", "fecha_cita", "hora_cita", "observaciones")
    list_filter = ("paciente", "medico", "especialidad", "fecha_cita")
    search_fields = ("paciente", "medico", "fecha_cita", "hora_cita")