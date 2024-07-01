from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from openai import OpenAI
from aigreetingcards.models import Image

from .models import Image, Prompt
from accounts.models import CustomUser

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('image_list'))
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)

def home(request):
    OPENAI_API_KEY = getattr(settings, 'OPENAI_API_KEY')
    prompt = ''
    img_url = ''
    response = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        client=OpenAI(
            api_key=OPENAI_API_KEY,
            )
        response = client.images.generate(
          model="dall-e-3",
          prompt=prompt,
          size="1024x1024",
          quality="standard",
          n=1,
        )

        img_url = response.data[0].url

        # Create a new instance of the image model
        new_image = Image(title=prompt, image_url=img_url)
        new_image.get_remote_image()
        # Save the instance to the database
        new_image.user_id = request.user.id
        new_image.save()
        return HttpResponseRedirect(reverse('image_list'))

    return render(request, 'home.html', {'prompt':prompt, 'img_url':img_url, 'response':response })

class ImageListView(ListView):
    model = Image
    template_name = 'image_list.html'
    def get_queryset(self, *args, **kwargs):
        qs = super(ImageListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs

class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'image_delete.html'
    success_url = reverse_lazy('image_list')
