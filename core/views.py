from django.shortcuts import render
from django.views.generic import View, DetailView

# Create your views here.


class Home(View):
    def get(self, request):
        return render(request, 'home.html')