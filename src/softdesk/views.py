from django.shortcuts import redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('api-root')
    else:
        return redirect('login')
