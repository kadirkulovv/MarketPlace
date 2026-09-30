from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ism va familiyangizni kiriting'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+998 90 123 45 67'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Viloyat, tuman, ko\'cha, uy raqami yoki mo\'ljal'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 2,
                'placeholder': 'Kuryer uchun qo\'shimcha ma\'lumot yoki istaklar (ixtiyoriy)'
            }),
        }
