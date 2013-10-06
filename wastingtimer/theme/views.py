# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect

def about_us(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']

            recipients = ['tim@buchwaldt.ws']

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('about-us/thanks/')
    else:
        print "seems like a get request"
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })