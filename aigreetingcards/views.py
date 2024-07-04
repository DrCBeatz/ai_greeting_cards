# aigreetingcards/views.py

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from aigreetingcards.models import Image

from .models import Image
from .tasks import generate_image_task

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

@login_required(login_url='login')
def home(request):
    prompt = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        generate_image_task.delay(prompt, request.user.id)
        return HttpResponseRedirect(reverse('image_list'))

    return render(request, 'home.html', {'prompt': prompt})

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
