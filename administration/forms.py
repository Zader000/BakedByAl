from django import forms
from BakedByAl.models import GalleryItem, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone number'}),
        }


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }