from rest_framework import serializers
from .models import Tree, Representation


class TreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tree
        fields = '__all__'


class RepresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Representation
        fields = '__all__'

