from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView
from blog.models import BlogPost
from main.forms import ContactForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class Index(ListView):
    template_name = 'main/index.html'
    model = BlogPost
    context_object_name = 'post_list'

class About(TemplateView):
    template_name = 'main/about.html'

class Contact(SuccessMessageMixin, FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('main:contact')
    success_message = 'Your email was submited successfully! We will be in touch in the next few days! Thank You!'
    
    def form_valid(self, form):

        full_name = form.cleaned_data.get('first_name').capitalize().strip() + ' ' + form.cleaned_data.get('last_name').capitalize().strip()
        message = "The following message was sent by " + full_name + ', using the email ' + form.cleaned_data.get('email') + ":\n\n" + form.cleaned_data.get('message')
        
        send_mail(
            "Feedback from" + ' ' + full_name,
            message,
            "blogwithdjango@gmail.com",
            ['blogwithdjango@gmail.com'],
        )

        return super(Contact, self).form_valid(form)