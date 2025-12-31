from django.shortcuts import render
from .services.search import search_all


def home(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = search_all(query)

    return render(request, "main/search.html", {"query": query, "results": results})

