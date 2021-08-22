from django.shortcuts import redirect

from .models import CustomUser
from rest_framework.permissions import AllowAny

from .serializers import SignUpSerializer
from rest_framework import generics


def index(request):
    return redirect('login')


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


