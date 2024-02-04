from django import forms

from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    locatie = forms.CharField(widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image', 'image_2','image_3', 'image_4', 'locatie')
        widgets = {
            
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image_2': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image_3': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image_4': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),


        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'image_2', 'image_3', 'image_4', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image_2': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image_3': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image_4': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),

        }