from django import forms
from .models import Oferta, Plato, Encuesta
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion' ,'categoria', 'precio', 'disponible', 'imagen']  # Agrega la imagen

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['rating', 'comentario']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("La calificación debe estar entre 1 y 5.")
        return rating
    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")  # Añadimos el campo email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]  # Guardamos el email proporcionado
        if commit:
            user.save()
        return user

class PagoForm(forms.Form):
    nombre = forms.CharField(max_length = 100)
    direccion = forms.CharField(max_length = 255)
    metodo_pago = forms.ChoiceField(choices=[
            ('tarjeta', 'Tarjeta de Credito'),
            ('efectivo', 'Efectivo'),
        ])
    numero_tarjeta = forms.CharField(min_length=16, max_length=16, required=False, label="Número de Tarjeta")
    fecha_vencimiento = forms.DateField(required=False, label="Fecha de Vencimiento (YYYY-MM-DD)")
    cvv = forms.CharField(max_length=3, required=False, label="CVV")

    def clean(self):
        cleaned_data = super().clean()
        metodo_pago = cleaned_data.get("metodo_pago")

        if metodo_pago == 'tarjeta':
            if not cleaned_data.get("numero_tarjeta"):
                self.add_error('numero_tarjeta', "Este campo es obligatorio si seleccionas tarjeta.")
            if not cleaned_data.get("fecha_vencimiento"):
                self.add_error('fecha_vencimiento', "Este campo es obligatorio si seleccionas tarjeta.")
            if not cleaned_data.get("cvv"):
                self.add_error('cvv', "Este campo es obligatorio si seleccionas tarjeta.")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['nombre', 'platos', 'precio_oferta', 'dias_especiales']
        widgets = {
            'platos': forms.CheckboxSelectMultiple(),  # Opcional: para mostrar como checkboxes
            'dias_especiales': forms.CheckboxSelectMultiple(),
        }