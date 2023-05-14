from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from core.models import Item, Shift, Reservation, Service, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('phone_number',)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = UserCreateSerializer.Meta.fields + ('phone_number',)
        
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['email'] == '':
            raise serializers.ValidationError("Email is required")
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists")
        return attrs


class ItemSerializer(serializers.ModelSerializer):
    """serializer for item model"""

    category = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id',]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model= Category
        fields = ['id', 'name']
        read_only_fields = ['id',]


class ShiftSerializer(serializers.ModelSerializer):

    services = serializers.PrimaryKeyRelatedField(many=True, read_only =True)

    class Meta:
        model = Shift
        fields = ['id', 'start_date', 'end_date', 'repeat', 'shift', 'services', 'item', 'is_available' ]
        read_only_fields = ['id',]


class ReservationSerializer(serializers.ModelSerializer):
    
    reserver = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Reservation
        fields = ['id', 'reserver', 'time_date', 'service', 'shift', 'item', 'code', 'status']
        read_only_fields = ['id',]


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id',]


class TimeSerializer(serializers.Serializer):
    time = serializers.TimeField()