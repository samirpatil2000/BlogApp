from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account
from phonenumber_field.formfields import PhoneNumberField


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    phone_number = PhoneNumberField(region='IN', help_text='Required. Add a valid phone number')

    class Meta:
        model = Account
        fields = ('email', 'phone_number' ,'password1', 'password2', )


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model=Account
        fields=('email','username','phone_number')

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            account=Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already use.'% account)

    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            account=Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already use.' % account)

    #TOdo we are use this in production
    """
    def clean_phone_number(self):
        phone_number=self.cleaned_data['phone_number']
        try:
            account=Account.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)
        except Account.DoesNotExist:
            return phone_number
        raise forms.ValidationError("Phone is already exist ")
        """


    """
    def save(self,commit=True):
        account=self.instance
        account.email=self.cleaned_data['email']
        account.username=self.cleaned_data['username']
        account.phone_number=self.cleaned_data['phone_number']

        if commit:
            account.save()

        return account
        
    """

