from django.db import models

class Usuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    ]

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='medico_profile')
    especialidad = models.CharField(max_length=150)
    horario_atencion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Dr. {self.usuario.nombre} - {self.especialidad}"

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='paciente_profile')
    cedula = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.cedula}"

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]

    id_cita = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita {self.id_cita} - {self.fecha} {self.hora} - {self.paciente.usuario.nombre}"

class Observacion(models.Model):
    id_observacion = models.AutoField(primary_key=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='observaciones')
    descripcion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Obs {self.id_observacion} - Cita {self.cita.id_cita}"

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('recordatorio', 'Recordatorio'),
        ('alerta', 'Alerta'),
        ('info', 'Informativa'),
    ]

    ESTADO_CHOICES = [
        ('enviada', 'Enviada'),
        ('pendiente', 'Pendiente'),
        ('fallida', 'Fallida'),
    ]

    id_notificacion = models.AutoField(primary_key=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_envio = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notificación {self.id_notificacion} - {self.tipo}"
