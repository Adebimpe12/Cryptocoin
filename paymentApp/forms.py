from django import forms

class Payment_form(forms.Form):
    card_number = forms.CharField(max_length=16, required=True, help_text='Number of Card')
    cvv = forms.CharField(max_length=3, required=True)
    expire_date = forms.CharField(required=True, help_text="dd/yy")