from rest_framework import serializers
from morket.models import User, Item

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    
