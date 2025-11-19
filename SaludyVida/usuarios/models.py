# Reemplaza todo tu archivo models.py con esto

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El usuario tiene que tener correo")
        
        correo = self.normalize_email(correo)
        # Saca 'nombre' de extra_fields si está, o ponlo vacío
        nombre = extra_fields.pop('nombre', '') 
        user = self.model(correo=correo, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Asegúrate de que los campos booleanos no estén en None si no se proveen
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(correo, password, **extra_fields)

# --- AHORA MIRA LAS CORRECCIONES ---
class Usuario(AbstractBaseUser, PermissionsMixin): # <-- 1. CORREGIDO: AbstractBaseUser
    
    # 2. CORREGIDO: max_length=191 para arreglar el error 1071
    correo = models.EmailField(max_length=191, unique=True)
    
    # Este campo 'nombre' está bien, pero asegúrate de que 'REQUIRED_FIELDS' 
    # coincida con lo que pones aquí.
    nombre = models.CharField(max_length=150)

    # Estos campos son necesarios para que AbstractBaseUser funcione
    # como el de Django.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    # Le decimos a Django que el 'correo' es el campo de login
    USERNAME_FIELD = 'correo'
    
    # Campos requeridos al crear un superusuario (además de correo y pass)
    REQUIRED_FIELDS = ['nombre'] 

    def __str__(self):
        return self.correo
