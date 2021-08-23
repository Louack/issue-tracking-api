from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Mot de passe": "Les mots de passe ne correspondent pas."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
