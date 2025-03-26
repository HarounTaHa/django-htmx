from django import forms
from django.core.exceptions import ValidationError
from contacts.models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(
                               attrs={'class': 'input input-bordered w-full',
                                      'placeholder': 'Contact Name'
                                      }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'input input-bordered w-full', 'placeholder': 'Contact Email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if email already exists for this user
        if Contact.objects.filter(user=self.initial.get('user'),email=email).exists():
            raise ValidationError('You already have a contact with this email.')
        return email

    class Meta:
        model = Contact
        fields = ('name', 'email',)
