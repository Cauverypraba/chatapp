from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
#from django.utils.six import python_2_unicode_compatible


#@python_2_unicode_compatible

class user(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200, null=True)
    mobile_number = models.CharField(max_length=20, null=True)
    profile_pic = models.ImageField(upload_to ='images', blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

class FriendList(models.Model):
    users = models.ManyToManyField(user)
    current_user = models.ForeignKey(user, related_name='current_user', null=True, on_delete=models.DO_NOTHING)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
              current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
              current_user=current_user
        )
        friend.users.remove(new_friend)

# class MessageQueryset(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True)

#     def    

class Message(models.Model):
    sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(user, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)            