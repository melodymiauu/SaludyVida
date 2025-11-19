from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=correo, password=password)

        if usuario is not None:
            login(request, usuario)
            messages.success(request, "Sesión iniciada correctamente.")
            return redirect('index')
        else:
            messages.error(request, "Correo o contraseña incorrectos")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect('login')
