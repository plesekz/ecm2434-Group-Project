from django import forms
from Login.models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['userID', 'email', 'username', 'password']