
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

@ratelimit(key='post:username', rate='5/m',
           method=['POST'], block=True)
def login(request):
    return render(request, "login.html")


@ratelimit(key='user', rate='10/m',
           method=ratelimit.ALL, block=True)
def restricted(request):
    return render(request, "restricted.html")

