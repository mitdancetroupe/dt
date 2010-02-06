from dt.contact.forms import ContactForm
from django.conf import settings

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        contact_form = ContactForm(request.POST) 
        if contact_form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = list(settings.CONTACT_EMAILS)
            if cc_myself:
                recipients.append(sender)

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)

            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        contact_form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'contact_form': contact_form,
    })

