from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('login/login_action', views.login_action),
    path('read/<str:blog_id>', views.read),
    path('profile/<str:username>', views.profile),
    path('myprofile/<str:username>', views.myprofile),
    path('edit_profile', views.edit_profile),
    path('add_blog/', views.add_blog),
    path("edit_blog/<int:id>", views.edit_blog),
    path("delete_blog/<int:id>", views.delete_blog),
    path("comment_blog/<int:id>", views.comment_blog),
    path('sign_up/', views.sign_up),
    path('sign_up/sign_up_action', views.sign_up_action),
    path('add_blog/add_blog_action/<str:user>/<str:name>', views.add_blog_action),
    path('logout/', views.logout),
    path('search/<str:type>', views.search),
    path('about/', views.about)

]
