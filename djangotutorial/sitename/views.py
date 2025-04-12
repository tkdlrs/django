# imports
from django.http import HttpResponse
from django.template import loader
from django.views import generic

from django.shortcuts import render

# code
class IndexView(generic.TemplateView):
    # return HttpResponse("This is a test") 
    template_name = "magic/index.html"
   
    
    
