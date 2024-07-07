# aigreetingcards/views.py

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from aigreetingcards.models import Image
from .models import Image
from .tasks import generate_image_task
import redis


redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

@login_required(login_url='login')
def check_task_status(request, task_id):
    status = redis_client.get(f"task_status:{task_id}")
    if status:
        return JsonResponse({'status': status.decode('utf-8')})
    return JsonResponse({'status': 'unknown'})

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
        size = request.POST.get('size')
        task = generate_image_task.delay(prompt, size, request.user.id)
        return HttpResponseRedirect(reverse('image_list') + f"?task_id={task.id}")
        
    return render(request, 'home.html', {'prompt': prompt})

class ImageListView(ListView):
    model = Image
    template_name = 'image_list.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(ImageListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.request.GET.get("task_id")
        context['task_id'] = task_id
        return context

class ImageDetailView(DetailView):
    template_name = 'image_detail.html'
    model = Image
    model_name = 'image'

class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'image_delete.html'
    success_url = reverse_lazy('image_list')

class ImageListRefreshView(TemplateView):
    template_name = 'partials/image_list_content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Image.objects.order_by("-id")
        return context