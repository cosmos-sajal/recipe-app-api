from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path(
        'password/token/',
        views.CreatePasswordTokenView.as_view(),
        name='token'),
    path('otp/token/', views.CreateOTPTokenView.as_view(), name='otp_token'),
    path('otp/generate/', views.GenerateOTPView.as_view(), name='otp_generate'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
