from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required # Necesario para la función de búsqueda

from .models import Medico, Paciente, Cita
from .forms import MedicoForm, PacienteForm, CitaForm


def index(request):
    return render(request, "index.html")


# ==========================
#    MÉDICOS
# ==========================
class MedicoListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Medico
    template_name = "medico_list.html"
    context_object_name = "medicos"

class MedicoCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Medico
    form_class = MedicoForm
    template_name = "medico_form.html"
    success_url = reverse_lazy("medico_list")
    
    def form_valid(self, form):
        messages.success(self.request, "Médico creado correctamente.")
        return super().form_valid(form)

class MedicoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Medico
    form_class = MedicoForm
    template_name = "medico_form.html"
    success_url = reverse_lazy("medico_list")
    
    def form_valid(self, form):
        messages.success(self.request, "Médico actualizado correctamente.")
        return super().form_valid(form)

class MedicoDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Medico
    success_url = reverse_lazy('medico_list')
    template_name = 'medico_eliminar.html'


# ==========================
#    PACIENTES
# ==========================
class PacienteListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Paciente
    template_name = "paciente_list.html"
    context_object_name = "pacientes"

class PacienteCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente_form.html"
    success_url = reverse_lazy("paciente_list")
    
    def form_valid(self, form):
        messages.success(self.request, "Paciente creado correctamente.")
        return super().form_valid(form)

class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente_form.html"
    success_url = reverse_lazy("paciente_list")
    
    def form_valid(self, form):
        messages.success(self.request, "Paciente actualizado correctamente.")
        return super().form_valid(form)

class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Paciente
    template_name = "paciente_confirm_delete.html"
    success_url = reverse_lazy("paciente_list")


# ==========================
#    CITAS
# ==========================
class CitaListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Cita
    template_name = "cita_list.html"
    context_object_name = "object_list" # Estandarizamos a object_list

class CitaCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Cita
    form_class = CitaForm
    template_name = "cita_form.html"
    success_url = reverse_lazy("cita_list")
    
    def form_valid(self, form):
        messages.success(self.request, "Cita creada correctamente.")
        return super().form_valid(form)

class CitaUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Cita
    form_class = CitaForm
    template_name = "cita_form.html"
    success_url = reverse_lazy("cita_list")
    
    def form_valid(self, form):
        messages.success(self.request, "Cita actualizada correctamente.")
        return super().form_valid(form)

class CitaDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Cita
    template_name = "cita_eliminar.html"
    success_url = reverse_lazy("cita_list")


# ==========================
#    BÚSQUEDA (CORREGIDO)
# ==========================
@login_required(login_url='login')
def buscar_citas(request):
    # Obtenemos los parámetros del GET
    fecha = request.GET.get('fecha')
    medico_id = request.GET.get('medico')
    paciente_id = request.GET.get('paciente')

    # Empezamos con todas las citas (pero solo si hay búsqueda se mostrarán en el template)
    citas = Cita.objects.all()

    # Filtramos paso a paso
    if fecha:
        citas = citas.filter(fecha_cita=fecha)

    if medico_id:
        citas = citas.filter(medico_id=medico_id)

    if paciente_id:
        citas = citas.filter(paciente_id=paciente_id)

    # Cargamos las listas para los <select> del formulario
    medicos = Medico.objects.all()
    pacientes = Paciente.objects.all()

    # IMPORTANTE: Asegúrate de que este nombre coincida con tu archivo HTML
    # En el paso anterior lo llamamos 'cita_search.html'. 
    # Si tú lo llamaste 'busqueda_citas.html', cambia el nombre aquí abajo.
    return render(request, "busqueda_citas.html", {
        "citas": citas,
        "medicos": medicos,
        "pacientes": pacientes,
    })