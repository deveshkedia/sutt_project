
from django.shortcuts import render,redirect
from django.contrib.auth import logout 

# Create your views here.
def home(request):
  return redirect('forum-home')