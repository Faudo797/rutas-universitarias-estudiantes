#accounts/models.py

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        default='avatars/default-avatar.png',
    )
    phone = models.CharField(max_length=20, blank=True)
    identificacion = models.CharField(max_length=10, blank=True)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    verified_email = models.BooleanField(default=False)
    is_active_gps = models.BooleanField(default=False, help_text="Indica si el usuario comparte ubicación en tiempo real.")
    last_connection = models.DateTimeField(auto_now=True, null=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def resource_keys(self) -> set[str]:
        keys = set()
        for role in self.roles.all().prefetch_related("resources"):
            keys.update(role.resources.values_list("key", flat=True))
        return keys

    def __str__(self):
        return self.username

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField("User", related_name="roles", through="UserRole")

    def __str__(self):
        return self.name


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    link_frontend = models.CharField(blank=True)
    link_backend = models.CharField(blank=True)

    roles = models.ManyToManyField("Role", related_name="resources", through="RoleResource")

    def __str__(self):
        return self.name


class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "role")


class RoleResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("role", "resource")

class UserActivityLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)  # ej. "route.view", "route.assign"
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    resources = models.ManyToManyField(Resource, related_name="permissions", blank=True)

from django.db import models

class Ruta(models.Model):
    nombre_ruta = models.CharField(max_length=100, verbose_name="Nombre de la ruta")
    capacidad_activa = models.IntegerField(blank=True, null=True, verbose_name="Capacidad activa")
    capacidad_espera = models.IntegerField(blank=True, null=True, verbose_name="Capacidad de espera")

    def __str__(self):
        return self.nombre_ruta

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"


class Bus(models.Model):
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa del bus")
    marca = models.CharField(max_length=50, verbose_name="Marca del bus")
    modelo = models.CharField(max_length=50, verbose_name="Modelo del bus")
    capacidad = models.IntegerField(blank=True, null=True, verbose_name="Capacidad del bus")
    estado_bus = models.CharField(max_length=50, verbose_name="Estado del bus")
    
    # Un bus pertenece a exactamente una ruta
    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE,
        related_name="buses",
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.placa} - {self.marca}"

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"


class Parada(models.Model):
    nombre_parada = models.CharField(max_length=100, verbose_name="Nombre de la parada")
    direccion = models.CharField(max_length=150, verbose_name="Dirección")
    tipo_punto = models.CharField(max_length=50, verbose_name="Tipo de punto")
    
    # Muchas paradas pertenecen a una ruta
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="paradas")

    def __str__(self):
        return self.nombre_parada

    class Meta:
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"


class TipoEstado(models.Model):
    nombre_estado = models.CharField(max_length=100, verbose_name="Nombre del estado")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del estado")
    
    # Muchos estados pertenecen a una ruta
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="tipos_estado")

    def __str__(self):
        return self.nombre_estado

    class Meta:
        verbose_name = "Tipo de Estado"
        verbose_name_plural = "Tipos de Estado"
