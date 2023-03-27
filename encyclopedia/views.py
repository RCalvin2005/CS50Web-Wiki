from django.shortcuts import render

from . import util
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(util.get_entry(title))
    })