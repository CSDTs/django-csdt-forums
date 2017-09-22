from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model


from . import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "community")
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["community"].queryset = (
                models.Community.objects.filter(
                    pk__in=user.communities.values_list("community__pk")
                )
            )

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)


        User = get_user_model()

        if User.objects.filter(email__iexact=self.cleaned_data['email']).exists():
            forms.error = "Email already in use. Please retrieve password if you forgot it."
            raise forms.ValidationError(u'Email "%s" is already in use.' % self.cleaned_data['email'])

        if User.objects.filter(username__iexact=self.cleaned_data['username']).exists():
            forms.error = "Username already taken. Please choose another username."
            raise forms.ValidationError(u'Username "%s" is already in use.' % self.cleaned_data['username'])

        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.bio = self.cleaned_data['bio']
        if commit:
            user.save()

        return user
