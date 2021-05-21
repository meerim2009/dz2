from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput

from test_app.models import Product, Category


class CourseForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=10,
                               required=True, label='Категория',
                               widget=TextInput(
                                   attrs={
                                       'placeholder': 'Название категории'
                                   }
                               ))

    def clean_name(self):
        name = self.cleaned_data['name']
        category = Category.objects.filter(name=name)

        if category.count() > 0:
            raise ValidationError('Такая категория уже существует')
        return name

    def save(self, commit=True):
        product = Category.objects.create(name=self.cleaned_data['name'])
        product.save()
        return product