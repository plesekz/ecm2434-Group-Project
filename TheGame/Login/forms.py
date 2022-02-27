from django import forms
from Login.models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['userID', 'role', 'email', 'username', 'password']