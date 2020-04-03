from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer, OPTAuthTOkenSerializer, GenerateOTPSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreatePasswordTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer


class CreateOTPTokenView(ObtainAuthToken):
    """Create a new auth token for user using otp"""
    serializer_class = OPTAuthTOkenSerializer


class GenerateOTPView(generics.CreateAPIView):
	"""Generates OTP for validation purpose"""
	serializer_class = GenerateOTPSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authetication user"""
        return self.request.user
