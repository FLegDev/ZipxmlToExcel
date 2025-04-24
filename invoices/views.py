from django.shortcuts import render

# Create your views here.
from django.utils.translation import get_language

def test_lang_view(request):
    return HttpResponse(f"Langue active : {get_language()}")
