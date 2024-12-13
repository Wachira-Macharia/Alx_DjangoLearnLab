from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Fetch the custom user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Ensure password is write-only and hidden
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Create a new user and hash their password securely
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Generate and attach a token for the user
        Token.objects.create(user=user)
        return user
