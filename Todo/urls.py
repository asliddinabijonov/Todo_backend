from django.contrib import admin
from django.urls import path
from taskApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TaskListView.as_view(), name='index'),
    path('edit/<int:pk>/', EditTaskView.as_view(), name='edit'),
    path('login/', LoginTaskView.as_view(), name='login'),
    path('logout/', LogoutTaskView.as_view(), name='logout'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete'),
    path('register/', RegisterTaskView.as_view(), name='register'),
]
