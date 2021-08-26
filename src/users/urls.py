from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignUpView, auth_index

urlpatterns = [
    path('', auth_index, name='check-auth'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('signup/', SignUpView.as_view(), name='signup')
]
