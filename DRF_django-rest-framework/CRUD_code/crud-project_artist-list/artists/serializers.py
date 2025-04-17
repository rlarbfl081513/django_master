from rest_framework import serializers
from .models import Artists


class ArtistsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artists
    fields = '__all__'

  
class ArtistsListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artists
    fields = ('name','debut_data',)


class ArtistsEditSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artists
    fields = ('agency','is_group',)