from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
from django.contrib import messages
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Enter Title'}))
    content = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder':'Enter Content in Markdown2'}))

class SearchForm(forms.Form):
    title = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

class EditForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea())

entries=util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "search": SearchForm(),
    })

def entry(request, title):
    exists=util.get_entry(title)
    if exists:
        html = markdown2.markdown(exists)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": html,
            "search": SearchForm(),
        })
    else:
        return( request, "encyclopedia/entry.html", {
            "title": "error",
            "content": f"Wiki page titled {title} not found."
            }) 

def newpage(request):
    if request.method == "POST":
        form1=NewPageForm(request.POST)

        if form1.is_valid():
            title=form1.cleaned_data["title"]
            content=form1.cleaned_data["content"]

            if title in entries:
                raise Exception("Entry already exists")

            else:
                util.save_entry(title, content)
                entries.append(title)

                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

        else:
            return render(request,"encyclopedia/newpage.html",{
                "form1":form1(),
                "search": SearchForm(),
                })

    return render(request, "encyclopedia/newpage.html",{
        "form1":NewPageForm(),
        "search": SearchForm(),
        })

def search(request):
    if request.method== "POST":
            
        search=SearchForm(request.POST)

        if search.is_valid():
            title=search.cleaned_data["title"]

            if title in entries:
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

            elif title not in entries:
                    
                related_entries=[]

                for entry in entries:
                    if entry.lower().__contains__(title.lower()):
                        related_entries.append(entry)

                return render(request, "encyclopedia/search_results.html", {
                    "title":title,
                    "related_entries":related_entries,
                    "search": SearchForm(),
                    })
    return HttpResponseRedirect(reverse("encyclopedia:index"))


def editpage(request, title):
    if request.method== "GET":

        initial_data = {
            "content":util.get_entry(title),
        }

        content={
            'search':SearchForm(),
            'edit':EditForm(initial=initial_data),
            'title':title,
        }
        return render(request, "encyclopedia/editpage.html", content)
    else:
        form2 = EditForm(request.POST)

        if form2.is_valid():
            content=form2.cleaned_data["content"]
            util.save_entry(title,content)

            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))


def rando(request):
    entries=util.list_entries()
    title= random.choice(entries)

    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))


