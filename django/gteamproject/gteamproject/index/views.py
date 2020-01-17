from django.shortcuts import render

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

def index_view(req):
    template = get_template("index.html")
    output = template.render()
    return HttpResponse(output)
