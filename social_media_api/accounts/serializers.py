from django.contrib.auth import get_user_model
from rest_framework import serializers

# Fetch the custom user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Explicitly define password as a CharField to handle it securely
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Use the `create_user` method to hash passwords and create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
