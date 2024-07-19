# aigreetingcards/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('images/', views.ImageListView.as_view(), name='image_list'),
    path('images/refresh/', views.ImageListRefreshView.as_view(), name='image_list_refresh'),
    path('images/<int:pk>/', views.ImageDetailView.as_view(), name='image_detail'),
    path('images/<int:pk>/delete/', views.ImageDeleteView.as_view(), name='image_delete'),
    path('my-images/', views.ImageUserListView.as_view(), name='image_user_list'),
    path('my-images/refresh/', views.ImageUserListRefreshView.as_view(), name='image_user_list_refresh'),
    path('image/<int:pk>/send-email/', views.send_image_email, name='send_image_email'),
    path('check-task-status/<str:task_id>/', views.check_task_status, name='check_task_status'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)