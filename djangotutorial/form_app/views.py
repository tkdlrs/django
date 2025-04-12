from django.shortcuts import render, redirect
from .form import ContactForm
# Create your views here.

def home_view(request):
    if request.method == "POST":
        form = ContactForm(request.Post)
        if form.is_valid():
            form.send_email()
            return redirect('home')
    else:
        form = ContactForm()
    context = {"form" : form}

    return render(request, 'form_app/home.html', context)
