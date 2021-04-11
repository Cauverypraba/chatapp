from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Min, Count
from django.utils.safestring import mark_safe
from real_chat.models import user, FriendList, Message
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from real_chat.serializers import MessageSerializer, UserSerializer
import json
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    return render(request, 'index.html')

def indexPage(request):
    return render(request, 'index.html')   

def room(request, room_name):
    print("inside room")
    return render(request, 'room.html', {
        'room_name': room_name,
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def login(request):
    friends = []
    username = request.POST.get('username')
    password = request.POST.get('password')
    chatUser = user.objects.get(name=username)
    print('inside login view',chatUser.name)
    users = user.objects.exclude(id=chatUser.id)
    # print('user',users)
    try:
       friend = FriendList.objects.get(current_user=chatUser)
    #    print('###',users,'###')
       friends = friend.users.all()
       print('friends', friends)
    #    users = user.objects.exclude(id=friends)
       print('users', users)
    except:
        friends = FriendList.objects.none()
    print(friend.id)    
    #print('frnds',friends)
    # users = user.objects.exclude(id=friends.id)
    pw = check_password(password,chatUser.password)
    print(pw)    
    if pw:
        response = render(request, 'home.html', {'currUser' : chatUser, 'users':users, 'friends': friends}) 
        response.set_cookie('last_connection', datetime.datetime.now())
        response.set_cookie('username', chatUser.name)
        print('inside login')
        return response
        # return redirect('chat/')
    return redirect('signupPage/')


def homePage(request):
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    users = user.objects.exclude(id=chatUser.id)
    print(chatUser.name)
    friend = FriendList.objects.get(current_user=chatUser)
    print(friend)
    try:
       friend = FriendList.objects.get(current_user=chatUser)
       friends = friend.users.all()
    except:
        friends = FriendList.objects.none()
    return render(request, 'home.html', {'currUser': chatUser, 'users':users, 'friends': friends})

def profilePage(request, pk=None):
    users = user.objects.all()    
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    if pk:
        chatUser = user.objects.get(pk=pk)
        #print("##",chatUser.name)
    else:
        chatUsers = request.user
    return render(request, 'profile.html', {'currUser':chatUser, 'users':users})

def signupPage(request):
    return render(request, 'register.html')   
    
def register(request):
    print('inside register')
    name = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('psw')
    re_password = request.POST.get('psw-repeat')
    mob_number = request.POST.get('mob.no')
    prof_pic = request.POST.get('prof-pic')
    print(prof_pic)
    #print('register',name,email)
    pswrd = make_password(password)
    if(password == re_password):
        db = user(name=name, email=email, password=pswrd, mobile_number=mob_number, profile_pic=prof_pic)
        db.save()
        return redirect('/indexPage')
    # if request.method == 'POST': 
    #     db = chatForm(request.POST, request.FILES) 
    #     if db.is_valid(): 
    #         db.save() 
    #         return redirect('success') 
    # else: 
    #     form = chatForm() 
    #     return render(request, 'register.html', {'form' : db})    

def ShowchatHome(request):
    return render(request, 'groupchat_home.html')

def ShowchatPage(request, room_name, person_name):
    return render(request, 'groupchat_screen.html',{'room_name': room_name, 'person_name': person_name})
    #return HttpResponse("Chat Page"+room_name+""+person_name)    

def change_friends(request, operation, pk):
    friend = user.objects.get(pk=pk)
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    if operation == 'add':
        FriendList.make_friend(chatUser, friend)
    elif operation == 'remove':
        FriendList.lose_friend(chatUser, friend)   
    return redirect('/homePage')

def chat(request):
    print('inside chat')
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    users = user.objects.exclude(id=chatUser.id)
    friend = FriendList.objects.get(current_user=chatUser)
    print(friend)
    try:
       friend = FriendList.objects.get(current_user=chatUser)
       friends = friend.users.all()
    except:
        friends = FriendList.objects.none()
    return render(request, 'chat.html', {'currUser': chatUser, 'users':users, 'friends': friends})

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        print(data)
        if serializer.is_valid():
            print('inside message list')
            serializer.save()
            print(serializer.data)
            return JsonResponse(serializer.data, status=201)
        # else:
        #     print('##error',serializer.errors)
        return JsonResponse(serializer.errors, status=400)

def message_view(request, sender, receiver):
    if request.method == "GET":
        username = request.COOKIES['username']
        chatUser = user.objects.get(name=username)
        print(chatUser.id)
        users = user.objects.exclude(id=chatUser.id)
        print(users)
        sender_obj = user.objects.get(id=sender)
        receiver_obj = user.objects.get(id=receiver)
        print(sender_obj.name, receiver_obj.name)
        friend = FriendList.objects.get(current_user=chatUser)
        # print('inside message', sender, receiver)
        try:
            messages1 = Message.objects.filter(sender_id=sender, receiver_id=receiver)
            messages2 = Message.objects.filter(sender_id=receiver, receiver_id=sender)
            friend = FriendList.objects.get(current_user=chatUser)
            friends = friend.users.all()
        except:
            receiver = Message.objects.none()
            friends = FriendList.objects.none()
        return render(request, "messages.html",
                      {'users': users, 'currUser': chatUser,
                       'messages': messages1 | messages2, 'friends' : friends, 'sender_obj':sender_obj, 
                       'receiver_obj': receiver_obj})
        # return render(request, "messages.html",
        #               {'users': users, 'currUser': chatUser,
        #                'receiver': receiver,
        #                'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
        #                            Message.objects.filter(sender_id=receiver, receiver_id=sender)})

def updateMessage(request, sender, receiver):
    print('inside update message')
    pk = request.POST.get('id')
    message = request.POST.get('message')
    print(pk, message)
    db = Message.objects.get(id=pk)
    print(db)
    db.message = message
    db.save()
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    print(chatUser.id)
    users = user.objects.exclude(id=chatUser.id)
    print(users)
    sender_obj = user.objects.get(id=sender)
    receiver_obj = user.objects.get(id=receiver)
    print(sender_obj.name, receiver_obj.name)
    friend = FriendList.objects.get(current_user=chatUser)
    # print('inside message', sender, receiver)
    try:
        messages1 = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        messages2 = Message.objects.filter(sender_id=receiver, receiver_id=sender)
        friend = FriendList.objects.get(current_user=chatUser)
        friends = friend.users.all()
    except:
        receiver = Message.objects.none()
        friends = FriendList.objects.none()
    return render(request, "messages.html",
                      {'users': users, 'currUser': chatUser,
                       'messages': messages1 | messages2, 'friends' : friends, 'sender_obj':sender_obj, 
                       'receiver_obj': receiver_obj})

def deleteMessage(request):
    print('inside delete message')
    pk = request.POST.get('id')
    print(pk)
    db = Message.objects.get(id=pk)
    # print(db)
    # msg = db.message
    db.delete()
    return render(request, 'messages.html')

def choose_room(request):
    return render(request, 'choose_room.html')

def pic_uploaded(request): 
    return HttpResponse('successfully uploaded')

def reset_page(request):
    return render(request, 'password_reset.html')

def password_reset(request):
    name = request.POST.get('username')
    password = request.POST.get('psw')
    re_password = request.POST.get('psw-repeat')
    pswrd = make_password(password)
    if(password == re_password):
        print('inside')
        db = user.objects.get(name = name, password = password)
        db.save()
        return redirect('/indexPage')
    #return render(request, 'password_reset.html')

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

def logout(request):
    return redirect('/indexPage')    