from .models import Ruta, Bus, Parada, TipoEstado
from .serializer import RutaSerializer, BusSerializer, ParadaSerializer, TipoEstadoSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [AllowAny]

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [AllowAny] 

class ParadaViewSet(viewsets.ModelViewSet):
    queryset = Parada.objects.all()
    serializer_class = ParadaSerializer
    permission_classes = [AllowAny]

class TipoEstadoViewSet(viewsets.ModelViewSet):
    queryset = TipoEstado.objects.all()
    serializer_class = TipoEstadoSerializer
    permission_classes = [AllowAny]
