from rest_framework import serializers
from .models import Ruta, Bus, Parada, TipoEstado


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class ParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parada
        fields = '__all__'

class TipoEstadoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TipoEstado
        fields = '__all__'
