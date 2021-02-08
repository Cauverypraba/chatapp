from django import forms  
from real_chat.models import chat  #models.py
    
class chatForm(forms.ModelForm):  
    class Meta:  
        model = chat  
        fields = "__all__"