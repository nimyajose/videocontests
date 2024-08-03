from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Video


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)




class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description','video_file']