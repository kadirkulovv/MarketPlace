from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={'placeholder': "Parolni kiriting...", 'class': 'form-input'}),
        min_length=8,
        error_messages={"min_length": "Parol eng kamida 8 belgidan iborat bo'lishi kerak"}
    )

    confirm_password = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={'placeholder': "Parolni tasdiqlang...", 'class': 'form-input'})
    )

    role = forms.ChoiceField(
        label="Foydalanuvchi roli",
        choices=User.ROLE_CHOICES,
        initial='buyer',
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'role', 'first_name', 'last_name', 'phone', 'address', 'avatar', 'shop_name')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Foydalanuvchi nomini kiriting...", 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': "Emailni kiriting...", 'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'placeholder': "Ismingizni kiriting...", 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': "Familiyangizni kiriting...", 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': "Telefon raqamingizni kiriting...", 'class': 'form-input'}),
            'address': forms.TextInput(attrs={'placeholder': "Manzilingizni kiriting...", 'class': 'form-input'}),
            'shop_name': forms.TextInput(attrs={'placeholder': "Do'kon nomini kiriting...", 'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Parollar bir xil emas!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi yoki Email",
        widget=forms.TextInput(attrs={'placeholder': "Foydalanuvchi nomini yoki Emailni kiriting...", 'class': 'form-input'})
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={'placeholder': "Parolni kiriting...", 'class': 'form-input'})
    )
    
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'avatar', 'shop_name']
        widgets = {
            "first_name": forms.TextInput(attrs={'class':'form-input'}),
            "last_name": forms.TextInput(attrs={'class':'form-input'}),
            "email": forms.EmailInput(attrs={'class':'form-input'}),
            "phone": forms.TextInput(attrs={'class':'form-input'}),
            "address": forms.TextInput(attrs={"rows": 3, 'class':'form-input'}),
            "avatar": forms.FileInput(attrs={'class':'form-input'}),
            "shop_name": forms.TextInput(attrs={'class':'form-input'}),
        }