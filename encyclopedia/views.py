from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    response = util.get_entry(name)
    if response is None:
        return render(request, "encyclopedia/error.html", {
            "error_entry": name,
            "error_type": 1
        })
    else:
        markdown = Markdown()
        response = markdown.convert(response)
        return render(request, "encyclopedia/entry.html", {
            "md_entry": name,
            "md_code": response
        })

def search_entry(request):
    if request.method == "POST":
        entry = request.POST['q']
        response = util.get_entry(entry)
        if response is None:
            list_of_entries = util.list_entries()
            results = []
            for entries in list_of_entries:
                if entry.lower() in entries.lower():
                    results.append(entries)
                else:
                    pass
            results_found = 0
            for _ in results:
                results_found += 1
            return render(request, "encyclopedia/search.html", {
                    "query": entry,
                    "results": results,
                    "results_found": results_found


            })
        else:
            return HttpResponseRedirect(f"/wiki/{entry}")

def new_page(request):
    if request.method == "POST":
        entry = request.POST["title"]
        content = request.POST["content"]
        response = util.get_entry(entry)
        if response is None:
            util.save_entry(entry, content)
            return HttpResponseRedirect(f"/wiki/{entry}")
        else:
            return render(request, "encyclopedia/error.html", {
                "error_entry": entry,
                "error_type": 2
            })

    else:
        return render(request, "encyclopedia/new_page.html")

def edit_page(request):
    if request.method == "POST":
        entry = request.POST["entry_title"]
        response = util.get_entry(entry)
        if response is not None:
            return render(request, "encyclopedia/edit_page.html", {
                "entry": entry,
                "entry_content": response
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error_entry": entry,
                "error_type": 1
            })

def save_page(request):
    if request.method == "POST":
        entry = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(entry, content)
        return HttpResponseRedirect(f"/wiki/{entry}")
    
def random_page(request):
    list_of_entries = util.list_entries()
    entry = random.choice(list_of_entries)
    return HttpResponseRedirect(f"/wiki/{entry}")
    

def redirect_user(request):
    return HttpResponseRedirect(reverse("index"))