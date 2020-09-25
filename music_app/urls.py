from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
#     path('logout', views.logout),
#     path('login', views.login),
#     path('dashboard/likes/<int:post_text_id>', views.likes),
#     path('dashboard/dislikes/<int:post_text_id>', views.dislike_post),
#     path('dashboard/newpost', views.add_post),
#     path('dashboard/delete/<int:post_text_id>', views.delete_post),
]
