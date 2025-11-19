from django import forms
from .models import Medico, Paciente, Cita
from datetime import date

# ============================
#        MÉDICOS
# ============================
class MedicoForm(forms.ModelForm):
    class Meta: 
        model = Medico
        fields = ['nombre_completo', 'rut', 'especialidad', 'correo', 'telefono']
        
        # Widgets (Estilos y Placeholder dentro de la caja)
        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Ej: 12345678K" 
            }),
            "especialidad": forms.Select(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
        }

        # Help Texts (Texto de ayuda debajo de la caja)
        help_texts = {
            "rut": "Por favor, ingrese el RUT sin puntos ni guion.",
        }

        labels = {
            "rut": "RUT del Médico",
        }

    # --- VALIDACIONES ---

    def clean_nombre_completo(self):
        nombre = self.cleaned_data["nombre_completo"]
        palabras = nombre.split()

        if len(palabras) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 palabras.")

        for palabra in palabras:
            if len(palabra) < 3:
                raise forms.ValidationError("Cada palabra debe tener al menos 3 letras.")

        return nombre
    
    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        rut = rut.replace(".", "").replace("-", "").upper()

        if len(rut) < 2:
            raise forms.ValidationError("RUT inválido.")

        numero = rut[:-1]
        dv = rut[-1]

        suma = 0
        mult = 2

        for n in reversed(numero):
            if not n.isdigit():
                raise forms.ValidationError("RUT contiene caracteres no válidos.")
            suma += int(n) * mult
            mult = 2 if mult == 7 else mult + 1

        dv_calc = 11 - (suma % 11)
        if dv_calc == 11:
            dv_calc = "0"
        elif dv_calc == 10:
            dv_calc = "K"

        if str(dv_calc) != dv:
            raise forms.ValidationError("El RUT ingresado no es válido.")

        # VALIDACIÓN DE DUPLICADOS (Solo si es nuevo registro)
        if self.instance.pk is None:
             if Medico.objects.filter(rut=rut).exists():
                raise forms.ValidationError("Este RUT ya está registrado.")

        return rut

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        
        # VALIDACIÓN DE DUPLICADOS (Solo si es nuevo registro)
        if self.instance.pk is None:
            if Medico.objects.filter(correo=correo).exists():
                raise forms.ValidationError("Este correo ya está registrado.")
        return correo


# ============================
#        PACIENTES
# ============================
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nombre_completo", "rut", "fecha_nacimiento", "sexo", "telefono"]
        
        # Widgets (Estilos y Placeholder dentro de la caja)
        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Ej: 12345678K" 
            }),
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "sexo": forms.Select(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
        }

        # Help Texts (Texto de ayuda debajo de la caja)
        help_texts = {
            "rut": "Por favor, ingrese el RUT sin puntos ni guion.",
        }
        
        labels = {
            "rut": "RUT del Paciente",
        }

    # --- VALIDACIONES ---

    def clean_nombre_completo(self):
        nombre = self.cleaned_data["nombre_completo"]
        palabras = nombre.split()

        if len(palabras) < 2:
            raise forms.ValidationError("Debe tener al menos 2 palabras.")

        for palabra in palabras:
            if len(palabra) < 3:
                raise forms.ValidationError("Cada palabra debe tener al menos 3 letras.")

        return nombre

    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        rut = rut.replace(".", "").replace("-", "").upper()

        if len(rut) < 2:
            raise forms.ValidationError("RUT inválido.")

        numero = rut[:-1]
        dv = rut[-1]

        suma = 0
        mult = 2

        for n in reversed(numero):
            if not n.isdigit():
                raise forms.ValidationError("RUT contiene caracteres no válidos.")
            suma += int(n) * mult
            mult = 2 if mult == 7 else mult + 1

        dv_calc = 11 - (suma % 11)
        if dv_calc == 11:
            dv_calc = "0"
        elif dv_calc == 10:
            dv_calc = "K"

        if str(dv_calc) != dv:
            raise forms.ValidationError("El RUT ingresado no es válido.")

        # VALIDACIÓN DE DUPLICADOS (Solo si es nuevo registro)
        if self.instance.pk is None:
            if Paciente.objects.filter(rut=rut).exists():
                raise forms.ValidationError("Este RUT ya está registrado.")

        return rut


# ============================
#          CITAS
# ============================
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["paciente", "medico", "especialidad", "fecha_cita", "hora_cita", "observaciones"]
        widgets = {
            "paciente": forms.Select(attrs={"class": "form-control"}),
            "medico": forms.Select(attrs={"class": "form-control"}),
            "especialidad": forms.Select(attrs={"class": "form-control"}),
            "fecha_cita": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora_cita": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def clean_fecha_cita(self):
        fecha = self.cleaned_data.get("fecha_cita")
        if fecha and fecha < date.today():
            raise forms.ValidationError("La fecha no puede ser anterior a hoy.")
        return fecha

    def clean(self):
        cleaned = super().clean()

        paciente = cleaned.get("paciente")
        medico = cleaned.get("medico")
        especialidad = cleaned.get("especialidad")
        fecha = cleaned.get("fecha_cita")
        hora = cleaned.get("hora_cita")

        if medico and especialidad:
            if especialidad != medico.especialidad:
                raise forms.ValidationError("La especialidad no coincide con la del médico.")

        if paciente and fecha and especialidad:
            # Agregamos chequeo de instancia para permitir editar la misma cita sin error
            if self.instance.pk is None: 
                if Cita.objects.filter(
                    paciente=paciente,
                    fecha_cita=fecha,
                    especialidad=especialidad
                ).exists():
                    raise forms.ValidationError(
                        "El paciente ya tiene una cita ese día en esa especialidad."
                    )

        if medico and fecha and hora:
             # Agregamos chequeo de instancia para permitir editar la misma cita sin error
            if self.instance.pk is None:
                if Cita.objects.filter(
                    medico=medico,
                    fecha_cita=fecha,
                    hora_cita=hora
                ).exists():
                    raise forms.ValidationError("El médico ya tiene una cita en ese horario.")

        return cleaned