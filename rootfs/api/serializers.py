"""
Classes to serialize the RESTful representation of Drycc API models.
"""
import logging
import json

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from rest_framework import serializers
from oauth2_provider.oauth2_validators import OAuth2Validator

logger = logging.getLogger(__name__)


class JSONFieldSerializer(serializers.JSONField):
    def __init__(self, *args, **kwargs):
        self.convert_to_str = kwargs.pop('convert_to_str', True)
        super(JSONFieldSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        """Deserialize the field's JSON data, for write operations."""
        try:
            val = json.loads(data)
        except TypeError:
            val = data
        return val

    def to_representation(self, obj):
        """Serialize the field's JSON data, for read operations."""
        for k, v in obj.items():
            if v is None:  # NoneType is used to unset a value
                continue

            try:
                if self.convert_to_str:
                    obj[k] = str(v)
            except ValueError:
                obj[k] = v
                # Do nothing, the validator will catch this later

        return obj


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', "first_name", "last_name",
                  "is_staff", "is_active", "is_superuser")


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class CustomOAuth2Validator(OAuth2Validator):

    def get_additional_claims(self, request):
        claims = super().get_additional_claims(request)
        claims["id"] = request.user.id
        claims["username"] = request.user.username
        claims["email"] = request.user.email
        claims["first_name"] = request.user.first_name
        claims["last_name"] = request.user.last_name
        claims["is_staff"] = request.user.is_staff
        claims["is_active"] = request.user.is_active
        claims["is_superuser"] = request.user.is_superuser
        return claims
