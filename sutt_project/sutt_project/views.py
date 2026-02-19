
from django.shortcuts import render, redirect
from django.contrib.auth import logout 

# Create your views here.
def home(request):
  return redirect('forum-home')

def handler404(request, exception=None):
  return render(request, '404.html', status=404)

def handler500(request):
  return render(request, '500.html', status=500)