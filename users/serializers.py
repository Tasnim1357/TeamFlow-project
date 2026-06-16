
from .models import NewUser
from rest_framework import serializers



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ("email", "user_name", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        return NewUser.objects.create_user(
            email=validated_data["email"],
            user_name=validated_data["user_name"],
            password=validated_data["password"]
        )