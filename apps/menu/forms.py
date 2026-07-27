"""Formularios del módulo de menú.

El ejemplo original declaraba `fields = '__all__'`. Aquí los campos se enumeran
de forma explícita: '__all__' expone automáticamente cualquier campo que se
agregue al modelo en el futuro, lo que habilita asignación masiva de datos que
no se pretendía hacer editables desde el formulario.
"""

from django import forms

from .models import Categoria, Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['name', 'description', 'precio', 'categoria', 'image', 'disponible']

    def clean_name(self):
        nombre = self.cleaned_data['name'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['name', 'orden']


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
