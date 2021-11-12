from django import forms

class addSellForm(forms.Form):
    item_bar = forms.IntegerField(widget=forms.TextInput(attrs={'autofocus':''})) 