from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True)
    username = serializers.CharField(
        required=True)
    password = serializers.CharField(
        min_length=8)

    def validate_password(self, value):
        return make_password(value)
    '''
    mirar como hacer para que la contraseña no salga ni hasheada en la respuesta
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance'''

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
