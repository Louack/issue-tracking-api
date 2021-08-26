from django.shortcuts import redirect

from .models import CustomUser
from rest_framework.permissions import AllowAny

from .serializers import SignUpSerializer
from rest_framework import generics


def auth_index(request):
    if request.user.is_authenticated:
        return redirect('api-root')
    else:
        return redirect('login')


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


