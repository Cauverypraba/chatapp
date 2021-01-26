from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#@login_required
def indexPage(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')    

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

def login(request):
    return render(request, 'login.html')

# def logout(request):
#     return render(request, "logout.html")    