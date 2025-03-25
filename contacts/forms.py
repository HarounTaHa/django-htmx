from django import forms

from contacts.models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(
                               attrs={'class': 'input input-bordered w-full',
                                      'placeholder': 'Contact Name'
                                      }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'input input-bordered w-full', 'placeholder': 'Contact Email'}))

    class Meta:
        model = Contact
        fields = ('name', 'email',)
