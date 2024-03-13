from rest_framework import serializers
from .models import RoofMaterial


class RoofMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoofMaterial
        fields = '__all__'