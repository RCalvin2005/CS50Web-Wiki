from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """ Displays content of given entry """

    # Get content of entry
    content = util.get_entry(title)

    if not content:
        # Renders error page
        return render(request, "encyclopedia/not_found.html", {
            "title": title
        })        

    # Render page content
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content)
    })
