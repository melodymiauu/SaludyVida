from django.db import models

# Opciones del sistema
SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro')
]

ESPECIALIDAD_CHOICES = [
    ('PEDIATRIA', 'Pediatría'),
    ('CARDIOLOGIA', 'Cardiología'),
    ('NUTRICION', 'Nutrición'),
    ('KINESIOLOGIA', 'Kinesiología'),
    ('GINECOLOGIA', 'Ginecología'),
    ('PSIQUIATRIA', 'Psiquiatría'),
    ('DERMATOLOGIA', 'Dermatología'),
    ('OTROS', 'Otros'),
]


# ============================
#         MÉDICO
# ============================
class Medico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)  # opcional

    class Meta:
        ordering = ['nombre_completo']

    def __str__(self):
        return f"{self.nombre_completo} ({self.especialidad})"


# ============================
#        PACIENTE
# ============================
class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        ordering = ['nombre_completo']

    def __str__(self):
        return self.nombre_completo


# ============================
#          CITA
# ============================
class Cita(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['fecha_cita']

    def __str__(self):
        return f"{self.fecha_cita} - {self.paciente} con {self.medico}"
