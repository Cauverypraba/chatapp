from django import forms  
from real_chat.models import user  #models.py
    
class chatForm(forms.ModelForm):  
    class Meta:  
        model = user  
        fields = "__all__"