from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from helper.helper_functions import get_random_number
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken



OTP_PREFIX = 'otp_login'


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class GenerateOTPSerializer(serializers.Serializer):
	"""Serializer for generating OTP for the client"""
	mobile_number = serializers.CharField()

	def validate(self, attrs):
		"""Validates if the mobile number is present in our DB"""
		mobile_number = attrs.get('mobile_number')

		try:
			user = get_user_model().objects.get(mobile_number=mobile_number)
		except ObjectDoesNotExist:
			msg = _('Mobile number does not exist in our system')
			raise NotFound(detail=msg)

		return attrs

	def create(self, validated_data):
		"""Sends the OTP for the given mobile number"""
		mobile_number = validated_data['mobile_number']
		cache_key = OTP_PREFIX + mobile_number
		otp = get_random_number()
		cache.set(cache_key, otp, 120)

		return {'mobile_number': mobile_number}


class OPTAuthTOkenSerializer(serializers.Serializer):
    """Serializer for user authentication object using otp"""
    mobile_number = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, attrs):
        """Validate and authenticate the user using otp"""
        print(attrs)
        mobile_number = attrs.get('mobile_number')
        otp = attrs.get('otp')
        cache_key = OTP_PREFIX + mobile_number
        cached_otp_value = cache.get(cache_key)
        user = None

        if cached_otp_value == otp:
            user = get_user_model().objects.get(mobile_number=mobile_number)

        if not user:
            msg = _('Unable to authenticate with provided credential')
            raise serializers.ValidationError(msg, code='authentication')

        refresh = TokenObtainPairSerializer.get_token(user)
        data = {
        	'refresh': str(refresh),
        	'access': str(refresh.access_token)
        }

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.access_token = attrs['access']
        self.refresh_token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            AccessToken(self.access_token).blacklist()
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            self.fail('bad_token')


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        print(user)

        if not user:
            msg = _('Unable to authenticate with provided credential')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
