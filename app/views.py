from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario
from django.urls import reverse

def register_view(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip().lower()
        contrasena = request.POST.get('contrasena', '')
        rol = request.POST.get('rol', 'paciente')

        if not nombre or not correo or not contrasena:
            messages.error(request, "Completa todos los campos requeridos.")
            return render(request, "register.html", {"nombre": nombre, "correo": correo, "rol": rol})

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
            return render(request, "register.html", {"nombre": nombre, "correo": correo, "rol": rol})

        hashed = make_password(contrasena)
        usuario = Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            contrasena=hashed,
            rol=rol
            # fecha_registro se llena automáticamente
        )

        messages.success(request, "Registro completado. Ahora inicia sesión.")
        return redirect(reverse('login'))
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        correo = request.POST.get('correo', '').strip().lower()
        contrasena = request.POST.get('contrasena', '')
        rol = request.POST.get('rol', '')

        if not correo or not contrasena or not rol:
            messages.error(request, "Introduce correo, contraseña y rol.")
            return render(request, "login.html", {"correo": correo, "rol": rol})

        try:
            usuario = Usuario.objects.get(correo=correo, rol=rol)
        except Usuario.DoesNotExist:
            messages.error(request, "Credenciales inválidas.")
            return render(request, "login.html", {"correo": correo, "rol": rol})

        if not check_password(contrasena, usuario.contrasena):
            messages.error(request, "Credenciales inválidas.")
            return render(request, "login.html", {"correo": correo, "rol": rol})

        # Login exitoso: guardamos id y rol en sesión
        request.session['usuario_id'] = usuario.id_usuario
        request.session['rol'] = usuario.rol
        request.session['usuario_nombre'] = usuario.nombre

        if usuario.rol == 'admin':
            return redirect(reverse('admin_home'))
        if usuario.rol == 'medico':
            return redirect(reverse('medico_home'))
        return redirect(reverse('paciente_home'))

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    messages.info(request, "Has cerrado sesión.")
    return redirect(reverse('login'))


def admin_home(request):
    if request.session.get('rol') != 'admin':
        return redirect(reverse('app:login'))
    nombre = request.session.get('usuario_nombre')
    return render(request, "admin_home.html", {"nombre": nombre})


def medico_home(request):
    if request.session.get('rol') != 'medico':
        return redirect(reverse('app:login'))
    nombre = request.session.get('usuario_nombre')
    return render(request, "medico_home.html", {"nombre": nombre})


def paciente_home(request):
    if request.session.get('rol') != 'paciente':
        return redirect(reverse('app:login'))
    nombre = request.session.get('usuario_nombre')
    return render(request, "paciente_home.html", {"nombre": nombre})
