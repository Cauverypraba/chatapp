from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from real_chat.models import chat
import json
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    return render(request, 'index.html')

def indexPage(request):
    return render(request, 'index.html')   

# def room(request, room_name):
#     return render(request, 'room.html', {
#         #'room_name': room_name
#         'room_name_json': mark_safe(json.dumps(room_name))
#     })

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    chatUser = {}
    chatUser = chat.objects.get(name=username)
    print('db',chatUser.password)
    pw = check_password(password,chatUser.password)
    print(pw)    
    if pw:
        print('hello')
        response = render(request, 'home.html', {'currUser' : chatUser}) 
        response.set_cookie('last_connection', datetime.datetime.now())
        response.set_cookie('username', chatUser.name)
        return response
    return redirect('signupPage/')


def homePage(request):
    username = request.COOKIES['username']
    chatUser = chat.objects.get(name=username)
    return render(request, 'home.html', {'currUser': chatUser})

def signupPage(request):
    return render(request, 'register.html')   
    
def register(request):
    print('inside register')
    name = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('psw')
    re_password = request.POST.get('psw-repeat')
    #print('register',name,email)
    pswrd = make_password(password)
    if(password == re_password):
        db = chat(name=name, email=email, password=pswrd)
        db.save()
        return redirect('/indexPage')
    #return render(request,'register.html')

def password_reset(request):
    return render(request, 'password_reset.html')

# def account(request, *args, **kwargs):
#     """
# 	- Logic here is kind of tricky
# 		is_self (boolean)
# 			is_friend (boolean)
# 				-1: NO_REQUEST_SENT
# 				0: THEM_SENT_TO_YOU
# 				1: YOU_SENT_TO_THEM
# 	"""
# 	context = {}
# 	user_name = kwargs.get("user_name")
# 	try:
# 		account = Account.objects.get(pk=user_name)
# 	except:
# 		return HttpResponse("Something went wrong.")
# 	if account:
# 		context['id'] = account.id
# 		context['username'] = account.username
# 		context['email'] = account.email
# 		context['profile_image'] = account.profile_image.url
# 		context['hide_email'] = account.hide_email

# 		# Define template variables
# 		is_self = True
# 		is_friend = False
# 		user = request.user
# 		if user.is_authenticated and user != account:
# 			is_self = False
# 		elif not user.is_authenticated:
# 			is_self = False
			
# 		# Set the template variables to the values
# 		context['is_self'] = is_self
# 		context['is_friend'] = is_friend
# 		context['BASE_URL'] = settings.BASE_URL
# 		return render(request, "account/account.html", context)

    

# def login(request):
#     return render(request, 'login.html')

# def logout(request):
#     return render(request, "logout.html")    