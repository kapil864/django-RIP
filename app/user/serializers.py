"""
Serializer for the user API view.
"""

from django.contrib.auth import get_user_model
from rest_framework import (
    serializers,
    authentication,
)
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # Set extra meta-data the fields
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        # For use in browsable API
        style={'input_type': 'password'},
        # by default django removes the trailing or/and leadingwhile spaces, prevent from doing it
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the users"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authentication.authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
