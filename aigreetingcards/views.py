# aigreetingcards/views.py

from django.conf import settings
from django.views.generic import (
    ListView, 
    DetailView, 
    DeleteView,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from aigreetingcards.models import Image
from .models import Image
from .tasks import generate_image_task
import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .forms import EmailImageForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

PAGINATION_AMOUNT = 6

@login_required(login_url='login')
def check_task_status(request, task_id):
    status = redis_client.get(f"task_status:{task_id}")
    if status:
        return JsonResponse({'status': status.decode('utf-8')})
    return JsonResponse({'status': 'unknown'})

@login_required(login_url='login')
def home(request):
    prompt = ''
    if request.method == 'POST':
        if request.user.credits >= 10:
            prompt = request.POST.get('prompt')
            size = request.POST.get('size')
            task = generate_image_task.delay(prompt, size, request.user.id)
            return HttpResponseRedirect(reverse('image_list') + f"?task_id={task.id}")
        else:
            messages.error(request, 'Insufficient credits to generate an image.')
            return redirect('home')
            
    return render(request, 'home.html', {'prompt': prompt})

class ImageListView(ListView):
    model = Image
    context_object_name = 'images'
    paginate_by = PAGINATION_AMOUNT

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['partials/image_list_content.html']
        return ['image_list.html']
    
    def get_queryset(self):
        return Image.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.request.GET.get("task_id")
        context['task_id'] = task_id
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            html = render_to_string(self.get_template_names(), context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)
        
class ImageListRefreshView(ListView):
    model = Image
    template_name = 'partials/image_list_content.html'
    context_object_name = 'images'
    paginate_by = PAGINATION_AMOUNT

    def get_queryset(self):
        return Image.objects.order_by('-id')
    
class ImageDetailView(DetailView):
    template_name = 'image_detail.html'
    model = Image
    model_name = 'image'

class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'image_delete.html'
    success_url = reverse_lazy('image_list')
    success_message = "Image deleted successfully"
    
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

class ImageUserListView(LoginRequiredMixin, ListView):
    model = Image
    context_object_name = 'images'
    paginate_by = PAGINATION_AMOUNT

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['partials/image_user_list_content.html']
        return ['image_user_list.html']

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).order_by('-id')
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            html = render_to_string(self.get_template_names(), context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class ImageUserListRefreshView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'partials/image_user_list_content.html'
    context_object_name = 'images'
    paginate_by = PAGINATION_AMOUNT

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).order_by('-id')

def send_image_email(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.method == 'POST':
        form = EmailImageForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            image_url = request.build_absolute_uri(image.thumbnail.url)
            email_body = f"{message}\n\nView the image: {image_url}"
            email_html = f"<p>{message}</p><p><img src='{image_url}'></p>"

            # Send email using SMTP
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                    html_message=email_html
                )
                messages.success(request, "Email sent successfully")
                return redirect(reverse('image_detail', args=[pk]))
            except Exception as e:
                form.add_error(None, f"Failed to send email: {str(e)}")
                messages.error(request, "Failed to send email")

    else:
        form = EmailImageForm()
    
    return render(request, 'send_image_email.html', {'form': form, 'image': image})
