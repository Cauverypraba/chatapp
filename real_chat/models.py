from django.db import models
#from django.utils.six import python_2_unicode_compatible


#@python_2_unicode_compatible

class chat(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default=False)
    password = models.CharField(max_length=200)

    # USERNAME_FIELD = 'email' 
    # REQUIRED_FIELDS = ['username']