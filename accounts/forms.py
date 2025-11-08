from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and styling
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        
        # Customize help text
        self.fields['username'].help_text = '150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters and cannot be entirely numeric.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'placeholder': 'email@example.com'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('native_language', 'learning_language', 'bio')
        widgets = {
            'native_language': forms.TextInput(attrs={'placeholder': 'e.g. English'}),
            'learning_language': forms.TextInput(attrs={'placeholder': 'e.g. Spanish'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your learning goals...'}),
        }
