from django import forms
from .models import Champion

class pStatsForm(forms.ModelForm):
    class Meta:
        model = Champion
        fields = ['username', 'pHealth', 'pToughness', 'pEvasion', 'damage', 'accuracy', 'attackSpeed', 'aHealth', 'aToughness', 'aEvasion']