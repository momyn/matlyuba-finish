from django import forms
from .models import Order
from django.core.mail import send_mail


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]




class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Количество',
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)



class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['size', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city']









