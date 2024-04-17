from django.shortcuts import render
from . import utils
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import os

OUTPUT_DIR = os.path.dirname(__file__)

# Create your views here.
def index(request): 
    
    return render(request, "dashboard/index.html", {
        "year": datetime.now().year
    })


def download(request):
    if request.method == "POST":
        query_data = request.POST["query_to_download"]
        list_query = query_data.splitlines()
        list_query = [item.strip() for item in list_query]

        files_downloaded = utils.download_query(list_query)
    
        files_downloaded = [{"url": f"dashboard/audio/output/{file}", "name": file} for file in files_downloaded]

        request.session['files'] = files_downloaded

        return HttpResponseRedirect(reverse("downloaded"))
    
    else:
        return HttpResponseRedirect(reverse("index"))

        

def downloaded(request):
    
    try:
        files_downloaded = request.session['files']
    except KeyError:
        return HttpResponseRedirect(reverse("index"))
    
    del request.session['files']
    request.session.modified = True

    return render(request, "dashboard/download.html", {
        "year": datetime.now().year,
        "files_downloaded": files_downloaded
    })
