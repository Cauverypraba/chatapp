from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#@login_required
def indexPage(request):
    return render(request, "index.html")

def base(request):
    return render(request, "base.html")    

def login(request):
    return render(request, "login.html")

# def logout(request):
#     return render(request, "logout.html")    