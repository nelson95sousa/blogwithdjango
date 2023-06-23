from django.urls import path
from main.views import (Index,About,Contact)

                        
app_name='main'

urlpatterns=[
    path('',Index.as_view(),name='index'),
    path("about", About.as_view(),name="about"),
    path("contact", Contact.as_view(),name="contact"),
]