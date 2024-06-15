from django.shortcuts import render
from .models import PC
from django.views.generic import ListView

class PCListView(ListView):
    model = PC
    template_name = "computers/pc-list.html"
    context_object_name = "PCs"