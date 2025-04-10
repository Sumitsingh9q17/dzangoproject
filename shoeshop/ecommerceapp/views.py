from django.shortcuts import render
from django.contrib import messages
from .models import Contact

# Create your views here.

def index(request):
    return render(request, 'index.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        phonenumber = request.POST.get('phonenumber')

        # Save the contact information to the database
        contact = Contact(name=name, email=email, desc=desc, phonenumber=phonenumber)
        contact.save()
        messages.info(request, "Your message has been sent successfully.")
        return render(request, 'contact.html')
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')