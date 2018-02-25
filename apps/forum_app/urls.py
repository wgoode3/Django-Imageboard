from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new_thread', views.new_thread),
    path('reply/<int:post_id>', views.reply),
    path('thread/<int:thread_id>', views.thread),
    path('q/<int:post_id>', views.query)
]