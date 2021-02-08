from django.db import models
#from django.utils.six import python_2_unicode_compatible


#@python_2_unicode_compatible

class chat(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    mobile_number = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to ='images/')
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    # class Meta:  
    #     db_table = "chat"

    # USERNAME_FIELD = 'email' 
    # REQUIRED_FIELDS = ['username']