from django.shortcuts import render
from django.http import HttpResponse
from simulations.forms import RequestForm


def home(request):
    return HttpResponse("Hello, world. You're at the pvfree home.")
