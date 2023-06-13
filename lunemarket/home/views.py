import random
from django.shortcuts import render
from django.views.generic import ListView
from typing import Any
from products.models.models import Category


class HomeView(ListView):
    model = Category
    template_name = 'home/home.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return self.model.objects.filter(parent=None)
