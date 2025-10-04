from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'role', 'password',
            'phone_number', 'address', 'date_of_birth', 'profile_picture', 'gender'
        )
        extra_kwargs = {'password': {'write_only': True}, 'role': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
