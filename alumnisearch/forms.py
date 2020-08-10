from django import forms
from .models import User, AlumnusProfile
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import datetime

class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'class': "form-control myfont"})


class RegistrationForm(forms.ModelForm, BootstrapForm):
    full_name = forms.CharField(max_length=100, label='Full Name')
    password = forms.CharField(label='Password')
    city = forms.CharField(max_length=100, label="City of your school")


    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'school', 'batch_year', 'city', 'country')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email) 
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("A user is already registered with this email !")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)


class SignInForm(forms.Form):
    email = forms.EmailField(max_length=150,  widget=forms.EmailInput(attrs={'placeholder': 'enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'enter password'}))


class ProfileForm(forms.ModelForm):
    gender = AlumnusProfile.GENDER_CHOICES
    DATE_INPUT_FORMATS = ('%d/%m/%Y','%Y/%m/%d')

    dob = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    website_url = forms.CharField(max_length=50, required=False, label="Your linkedin url or website ")
    description = forms.CharField(max_length=500, label="More about you", required=False)
    gender = forms.ChoiceField(label='Gender', choices=gender , required=False)

    class Meta:
        model = AlumnusProfile
        exclude = ('alumnus', 'profile_image')
        help_texts = {
            "dob": "This should be in the format dd/mm/yy or yy/mm/dd..."
        }


class UserForm(forms.ModelForm):
    city = forms.CharField(max_length=100, label="City of your school", required=False)

    class Meta:
        model = User
        fields = ('profile_name', 'full_name', 'email', 'school', 'batch_year', 'city', 'country')
    

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    fields = ('old_password', 'new_password', 'confirm_password')

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("The passwords don't match!")

