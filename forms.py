from django import forms


class connexion(forms.Form):

    login = forms.CharField(label='Username', max_length=64,widget=forms.TextInput(attrs={'placeholder': 'usernanme'}))
    motDePasse = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder': 'password'}))