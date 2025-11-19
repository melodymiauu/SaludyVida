from django.urls import path
from .views import (
    index,
    MedicoListView, MedicoCreateView, MedicoUpdateView, MedicoDeleteView,
    PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView,
    CitaListView, CitaCreateView, CitaUpdateView, CitaDeleteView,
    buscar_citas
)

urlpatterns = [
    path("", index, name="index"),
    path("medicos/", MedicoListView.as_view(), name="medico_list"),
    path("medicos/crear/", MedicoCreateView.as_view(), name="medico_create"),
    path("medicos/<int:pk>/editar/", MedicoUpdateView.as_view(), name="medico_update"),
    path("medicos/<int:pk>/eliminar/", MedicoDeleteView.as_view(), name="medico_delete"),
    path("pacientes/", PacienteListView.as_view(), name="paciente_list"),
    path("pacientes/crear/", PacienteCreateView.as_view(), name="paciente_create"),
    path("pacientes/<int:pk>/editar/", PacienteUpdateView.as_view(), name="paciente_update"),
    path("pacientes/<int:pk>/eliminar/", PacienteDeleteView.as_view(), name="paciente_delete"),
    path("citas/", CitaListView.as_view(), name="cita_list"),
    path("citas/crear/", CitaCreateView.as_view(), name="cita_create"),
    path("citas/<int:pk>/editar/", CitaUpdateView.as_view(), name="cita_update"),
    path("citas/<int:pk>/eliminar/", CitaDeleteView.as_view(), name="cita_delete"),
    path("buscar-citas/", buscar_citas, name="buscar_citas"),


]
