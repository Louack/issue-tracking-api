from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignUpView, index

urlpatterns = [
    path('', index, name='users-index'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('signup/', SignUpView.as_view(), name='signup')
]
