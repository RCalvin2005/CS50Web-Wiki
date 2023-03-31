from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
from markdown2 import markdown
from random import choice


class EntryForm(forms.Form):

    # https://stackoverflow.com/questions/66707030/django-textarea-form
    title =  forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


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
        "content": util.convert(content)
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


def random(request):
    """ Redirects to random entry page """

    entries = util.list_entries()

    return HttpResponseRedirect(reverse("entry", args=[choice(entries)]))


def new(request):
    """ Allow user to create new entry """

    if request.method == "POST":

        # Save form data
        form = EntryForm(request.POST)

        if form.is_valid():

            # Clean data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            entries = util.list_entries()

            # Check if entry doesn't already exist
            if title not in entries:

                # Save new entry
                util.save_entry(title, content)

                # Display new entry
                return HttpResponseRedirect(reverse("entry", args=[title]))
            
            else:
                # Create error message
                error = f"The entry <span class='font-weight-bold'>{title}</span> already exists! Choose a different title or edit the existing entry."

        # Redisplay filled form with error message
        return render(request, "encyclopedia/new.html", {
            "form": form,
            "error": error
        })
    
    else:
        # Renders create new entry page
        return render(request, "encyclopedia/new.html", {
            "form": EntryForm()
        })
    

def edit(request, title):
    """ Allows user to edit entry Markdown content """

    if request.method == "POST":

        # Save form data
        form = EntryForm(request.POST)

        if form.is_valid():

            # Clean data
            content = form.cleaned_data["content"]

            # Save new entry
            util.save_entry(title, content)

            # Display new entry
            return HttpResponseRedirect(reverse("entry", args=[title]))

        # Redisplay filled form with error message
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "error": "Failed to save edit."
        })
    
    else:
        content = util.get_entry(title)

        if not content:
            # Renders error page
            return render(request, "encyclopedia/not_found.html", {
                "title": title
            })        

        # https://stackoverflow.com/questions/604266/django-set-default-form-values
        form = EntryForm(initial={"title": title, "content": content})

        # https://stackoverflow.com/questions/324477/in-a-django-form-how-do-i-make-a-field-readonly-or-disabled-so-that-it-cannot
        form.fields["title"].widget.attrs["readonly"] = True

        # Renders edit entry page with filled content
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })
