from django.urls import path
from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'user'



urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path(
        'password/token/',
        views.CreatePasswordTokenView.as_view(),
        name='token'),
    path('otp/token/', views.CreateOTPTokenView.as_view(), name='otp_token'),
    path('otp/generate/', views.GenerateOTPView.as_view(), name='otp_generate'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/token/logout/', views.LogoutView.as_view(), name='token_logout')
]
