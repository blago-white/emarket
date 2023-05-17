import random
from django.shortcuts import render
from django.views.generic import ListView
from typing import Any
from products.models import Categories
from .filters import *


class HomeView(ListView):
    model = Categories
    template_name = 'home/home.html'
    context_object_name = 'categories'
