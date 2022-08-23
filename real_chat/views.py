from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Min, Count
from django.utils.safestring import mark_safe
from real_chat.models import user, FriendList, Message, HiddenFriends
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from real_chat.serializers import MessageSerializer, UserSerializer
import json
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

# Returns a default index page.
def index(request):
    return render(request, 'index.html')

# This function is used for redirecting to index page.
def indexPage(request):
    return render(request, 'index.html')   

# Returns a room name in which users wish to chat using websockets.
def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name,
        'room_name_json': mark_safe(json.dumps(room_name))
    })

# This function performs aunthentication, after successfull login 
# users can enter into their home page. 
def login(request):
    friends = []
    username = request.POST.get('username')
    password = request.POST.get('password')
    chatUser = user.objects.get(name=username)
    users = user.objects.exclude(id=chatUser.id)
    try:
       friend = FriendList.objects.get(current_user=chatUser)
       friends = friend.users.all()
       hidefrnd = HiddenFriends.objects.get(current_user=chatUser)
       hiddenfrnds = hidefrnd.users.all()
    except:
        friends = FriendList.objects.none()
        hiddenfrnds = HiddenFriends.objects.none()    
    pw = check_password(password,chatUser.password)    
    if pw:
        response = render(request, 'home.html', {'currUser' : chatUser, 'users':users, 'friends': friends,
        'hiddenfrnds': hiddenfrnds}) 
        response.set_cookie('last_connection', datetime.datetime.now())
        response.set_cookie('username', chatUser.name)
        return response
    return redirect('signupPage/')

# Users home page where it displays a friends list and other users as well,
# they can add, remove and hide from their friends list. 
def homePage(request):
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    users = user.objects.exclude(id=chatUser.id)
    print(chatUser.name)
    try:
       friend = FriendList.objects.get(current_user=chatUser)
       friends = friend.users.all()
       hidefrnd = HiddenFriends.objects.get(current_user=chatUser)
       print('hidefriend',hidefrnd)
       hiddenfrnds = hidefrnd.users.all()
       print(hiddenfrnds)
    except:
        friends = FriendList.objects.none()
        hiddenfrnds = HiddenFriends.objects.none()
    return render(request, 'home.html', {'currUser': chatUser, 'users':users, 'friends': friends,
    'hiddenfrnds': hiddenfrnds})

# This function returns profile page of an user with their details.
def profilePage(request, pk=None):
    users = user.objects.all()    
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    if pk:
        chatUser = user.objects.get(pk=pk)
    else:
        chatUsers = request.user
    return render(request, 'profile.html', {'currUser':chatUser, 'users':users})

# This function is used for redirecting to register page.
def signupPage(request):
    return render(request, 'register.html')   

# This function is used to register users into JusChat    
def register(request):
    print('inside register')
    name = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('psw')
    re_password = request.POST.get('psw-repeat')
    mob_number = request.POST.get('mob.no')
    prof_pic = request.POST.get('prof-pic')
    print(prof_pic)
    pswrd = make_password(password)
    if(password == re_password):
        db = user(name=name, email=email, password=pswrd, mobile_number=mob_number, profile_pic=prof_pic)
        db.save()
        return redirect('/indexPage')    

def ShowchatHome(request):
    return render(request, 'groupchat_home.html')

def ShowchatPage(request, room_name, person_name):
    return render(request, 'groupchat_screen.html',{'room_name': room_name, 'person_name': person_name})   

def change_friends(request, operation, pk):
    friend = user.objects.get(pk=pk)
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    if operation == 'add':
        FriendList.make_friend(chatUser, friend)
    elif operation == 'remove':
        FriendList.lose_friend(chatUser, friend)       
    return redirect('/homePage')

def checkPassword(request):
    name = request.POST.get('username')
    password = request.POST.get('psw')
    try:
        chatUser = user.objects.get(name=name)
        pw = check_password(password,chatUser.password)
        if pw:
            print(pw)
            return redirect('hidePage/')
    except:
        chatUser = user.objects.none()
    print('checkpassword page')        
    return render(request, 'checkPassword.html')    

def hidePage(request):
    hidefrnd = []
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    users = user.objects.exclude(id=chatUser.id)
    print('users',users)
    print('inside hide Page')
    try :
        hidefrnd = HiddenFriends.objects.get(current_user=chatUser)
        print('hidefriend',hidefrnd)
        hiddenfrnds = hidefrnd.users.all()
        print(hiddenfrnds)
    except:
        hiddenfrnds = HiddenFriends.objects.all()
        print('no hidden frnds',type(hiddenfrnds))        
    return render(request, 'hideFriends.html', {'currUser': chatUser, 'hiddenfrnds': hiddenfrnds})

def hideChat(request,operation, pk):
    hidefrnd = []
    username = request.COOKIES['username']
    chatUser = user.objects.get(name=username)
    users = user.objects.exclude(id=chatUser.id)
    print('inside hide chat')
    try :
        hidefrnd = user.objects.get(pk=pk)
        print('friend',hidefrnd.name)
        HiddenFriends.hide_friend(chatUser, hidefrnd)
        hidefrnd = HiddenFriends.objects.get(current_user=chatUser)
        hiddenfrnds = hidefrnd.users.all()
    except:
        hiddenfrnds = HiddenFriends.objects.all()
    if operation == 'add':
        return redirect('/homePage')            
    return render(request, 'hideFriends.html', {'currUser': chatUser, 'hiddenfrnds': hiddenfrnds})

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
       hidefrnd = HiddenFriends.objects.get(current_user=chatUser)
       hiddenfrnds = hidefrnd.users.all()
    except:
        friends = FriendList.objects.none()
        hiddenfrnds = HiddenFriends.objects.none()
    return render(request, 'chat.html', {'currUser': chatUser, 'users':users, 'friends': friends,
     'hiddenfrnds': hiddenfrnds})

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
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def message_view(request, sender, receiver):
    if request.method == "GET":
        print('inside message view')
        username = request.COOKIES['username']
        chatUser = user.objects.get(name=username)
        print(chatUser.id)
        users = user.objects.exclude(id=chatUser.id)
        print(users)
        sender_obj = user.objects.get(id=sender)
        receiver_obj = user.objects.get(id=receiver)
        print(sender_obj.name, receiver_obj.name)
        friend = FriendList.objects.get(current_user=chatUser)
        try:
            messages1 = Message.objects.filter(sender_id=sender, receiver_id=receiver)
            messages2 = Message.objects.filter(sender_id=receiver, receiver_id=sender)
            friend = FriendList.objects.get(current_user=chatUser)
            friends = friend.users.all()
            hidefrnd = HiddenFriends.objects.get(current_user=chatUser)
            hiddenfrnds = hidefrnd.users.all()
        except:
            receiver = Message.objects.none()
            friends = FriendList.objects.none()
            hiddenfrnds = HiddenFriends.objects.none()
        return render(request, "messages.html",
                      {'users': users, 'currUser': chatUser,
                       'messages': messages1 | messages2, 'friends' : friends, 'sender_obj':sender_obj, 
                       'receiver_obj': receiver_obj, 'hiddenfrnds': hiddenfrnds})

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
    
def logout(request):
    return redirect('/indexPage')    