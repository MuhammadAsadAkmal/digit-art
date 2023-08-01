from django.shortcuts import render
from django.shortcuts import render
from ..models import *

def contactus(request):
    if request.method == 'POST':
        # Get the form data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone = request.POST.get('phone')

        # Create a new contactUs instance
        contact = contactUs(
            name=name,
            email=email,
            subject=subject,
            message=message,
            phone=phone
        )
        
        # Validate the contactUs instance
        errors = contact.validate()
        
        if errors:
            # If there are errors, pass them to the template
            context = {
                'errors': errors,
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'phone': phone
            }
            return render(request, 'main/contact.html', context=context)
        
        # Save the contactUs instance to the database
        contact.save()
        
        # Optionally, you can perform other actions like sending an email notification, etc.
        
        # Redirect to a success page
        return render(request, 'main/contact.html')
    else:
        # If it's a GET request, simply render the contact form
        return render(request, 'main/contact.html')



def service(request):
    return render(request, 'main/service.html')
