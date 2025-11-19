from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from sistema.views import index
from usuarios.views import login_view, logout_view
from usuarios.forms import LoginForm

urlpatterns = [
    # Página principal
    path("", index, name="index"),

    # Admin
    path("admin/", admin.site.urls),

    # Login y Logout
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=LoginForm
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Rutas de la app sistema
    path("", include("sistema.urls")),
]
