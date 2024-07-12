# aigreetingcards/forms.py

from django import forms

class EmailImageForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
    subject = forms.CharField(max_length=100, label='Email Subject')
    message = forms.CharField(widget=forms.Textarea, label='Email Body')