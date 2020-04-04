from rest_framework import generics, authentication, permissions, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer, OPTAuthTOkenSerializer, GenerateOTPSerializer, LogoutSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreatePasswordTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer


class CreateOTPTokenView(TokenObtainPairView):
    """Create a new auth token for user using otp"""
    serializer_class = OPTAuthTOkenSerializer


class GenerateOTPView(generics.CreateAPIView):
	"""Generates OTP for validation purpose"""
	serializer_class = GenerateOTPSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authetication user"""
        return self.request.user


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()

        return Response(status=status.HTTP_204_NO_CONTENT)