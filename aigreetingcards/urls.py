# aigreetingcards/urls.py

from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='image_list'), name='logout'),
    
    path('images/', views.ImageListView.as_view(), name='image_list'),
    path('images/refresh/', views.ImageListRefreshView.as_view(), name='image_list_refresh'),
    path('images/<int:pk>/', views.ImageDetailView.as_view(), name='image_detail'),
    path('images/<int:pk>/delete/', views.ImageDeleteView.as_view(), name='image_delete'),
    path('my-images/', views.ImageUserListView.as_view(), name='image_user_list'),
    
    path('check-task-status/<str:task_id>/', views.check_task_status, name='check_task_status'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)