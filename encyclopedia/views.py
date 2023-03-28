from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
from markdown2 import markdown


def index(request):
    """ Displays list of all entries """

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


def search(request):
    """ Allow user to search entry in sidebar """

    if request.method == "POST":

        # https://stackoverflow.com/questions/4706255/how-to-get-value-from-form-field-in-django-framework
        q = request.POST.get("q")
        entries = util.list_entries()
        matches = []

        # Goes through each entry and check if it matches the query
        for entry in entries:

            # Redirect if full match
            if entry.lower() == q.lower():

                # https://docs.djangoproject.com/en/4.1/ref/urlresolvers/#reverse
                return HttpResponseRedirect(reverse("entry", args=[entry]))
            
            # Record partial matches
            if q.lower() in entry.lower():
                matches.append(entry)

        # Renders page with partial match results
        return render(request, "encyclopedia/results.html", {
            "q": q,
            "matches": matches
        })

    else:
        # Redirect to index if /search URL is visited
        return HttpResponseRedirect(reverse("index"))
