from .views import Home
from django.urls import path, include

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='home')
]
