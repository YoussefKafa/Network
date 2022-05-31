
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createPost", views.createPost, name="createPost"),
    path("profile/<int:user>", views.profileLoad, name="profile"),
    path("followUnfollow/<int:user>", views.followUnfollow, name="followUnfollow")
]
