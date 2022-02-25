from django import forms
from Login.models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['email', 'username', 'password']