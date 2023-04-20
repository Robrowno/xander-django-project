""" Serializers for the User API views """

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    class Meta: 
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {
            'write_only' : True,
            'min_length' : 7,
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    """ Serializer for auth token API """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={
        'input_type': 'password',
        'trim_whitespace': False
        }
    )

    def validate(self, attrs):
        """ Validate and return user """

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authorise with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs