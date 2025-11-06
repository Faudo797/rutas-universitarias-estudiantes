from django.contrib import admin
from .models import Ruta, Bus, Parada, TipoEstado


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ("nombre_ruta", "capacidad_activa", "capacidad_espera")
    search_fields = ("nombre_ruta",)
    list_filter = ("capacidad_activa", "capacidad_espera")
    ordering = ("nombre_ruta",)


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("placa", "marca", "modelo", "capacidad", "estado_bus", "ruta")
    search_fields = ("placa", "marca", "modelo")
    list_filter = ("estado_bus", "ruta")
    ordering = ("placa",)
    list_select_related = ("ruta",)


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ("nombre_parada", "direccion", "tipo_punto", "ruta")
    search_fields = ("nombre_parada", "direccion", "tipo_punto")
    list_filter = ("tipo_punto", "ruta")
    ordering = ("nombre_parada",)
    list_select_related = ("ruta",)


@admin.register(TipoEstado)
class TipoEstadoAdmin(admin.ModelAdmin):
    list_display = ("nombre_estado", "descripcion", "ruta")
    search_fields = ("nombre_estado", "descripcion")
    list_filter = ("ruta",)
    ordering = ("nombre_estado",)
    list_select_related = ("ruta",)
