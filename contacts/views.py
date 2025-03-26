from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import contacts
from contacts.models import Contact
from django.db.models import Q
from contacts.forms import ContactForm
from django.views.decorators.http import require_http_methods


@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {'contacts': contacts, 'form': ContactForm()}
    return render(request, 'contacts.html', context)


@login_required
def search_contact(request):
    import time
    time.sleep(2)
    query = request.GET.get('search', '')
    # use the query to filter contacts by name or email
    contacts = request.user.contacts.filter(Q(name__icontains=query) | Q(email__icontains=query))
    return render(request, 'partials/contact-list.html', {'contacts': contacts})


@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST, initial={'user': request.user})
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()

        # Get all contacts to render the full list
        contacts = Contact.objects.filter(user=request.user)

        # Return the full contacts list
        response = render(request, 'partials/contact-list.html', {'contacts': contacts})
        response['HX-Trigger'] = 'success'

        # Close the modal
        response['HX-Trigger'] = json.dumps({
            'success': True,
            'closeModal': 'contact_modal'
        })

        return response
    else:
        response = render(request, 'partials/add-contact-modal.html', {'form': form})
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response
