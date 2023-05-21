from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import QuerySet
from .models.models import Cards, Categories


class ProductsView(ListView):
    model = Cards
    template_name = "products\\products-listing.html"
    context_object_name = "items"

    def get_queryset(self):
        category = self.kwargs.get("category")

        query_set: QuerySet = Categories.objects.filter(parent=category)

        if not len(query_set):
            query_set: QuerySet = self.model.objects.filter(category=category)

        return query_set.order_by("title")
