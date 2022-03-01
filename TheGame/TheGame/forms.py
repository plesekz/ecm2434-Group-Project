from django import forms
from .models import pStats

class pStatsForm(forms.ModelForm):
    class Meta:
        model = Player_Stat
        fields = ['username', 'pHealth', 'pToughness', 'pEvasion', 'damage', 'accuracy', 'attackSpeed', 'aHealth', 'aToughness', 'aEvasion']