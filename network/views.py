from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Follow, User
from .models import Post


def index(request):
    allPosts= Post.objects.all().order_by('id').reverse()
    pn = request.GET.get('page')
    paginator= Paginator(allPosts, 10)
    pageItems=paginator.get_page(pn)
    return render(request, "network/index.html", {'allPosts': pageItems})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def createPost(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST["newPostText"]
        if not text:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        post = Post.objects.create(text=text, user=user)
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def profileLoad(request,user):
    # get user profile
    openedUser=User.objects.get(pk=user)
    allPosts=Post.objects.filter(user=user).order_by('id').reverse()
    # get user followers
    try:
     following= Follow.objects.filter(user=user)
    except Follow.DoesNotExist:
     following   = None
    try:
     followers=Follow.objects.filter(userFollowed=user).values_list('userFollowed', flat=True)
    except Follow.DoesNotExist:
     followers   = None
    paginator=Paginator(allPosts,10)
    pn=request.GET.get('page')
    pageItems=paginator.get_page(pn)
    return render(request, "network/profile.html", {'allPosts':pageItems,'openedUser':openedUser, 'following':following, 'followers':followers})


def followUnfollow(request, user):
    try:
        followObj = Follow.objects.get(user=request.user.id, userFollowed=user)
    except Follow.DoesNotExist:
            try:
                followedUser = User.objects.get(pk=user)
            except followedUser.DoesNotExist:
                return HttpResponse(status=404)
            else:
                newFollow = Follow(user=request.user, userFollowed=followedUser)
                newFollow.save()
    else:
        followObj.delete()
   
    return HttpResponseRedirect(reverse("profile", args=[user]))



def following (request,user):
  loggedUser= get_object_or_404(User, id=user)
  followingList=Follow.objects.filter(user=loggedUser)
  posts=Post.objects.all().order_by('id').reverse()
  result=[]
  for post in posts:
      for follower in followingList:
          if follower.userFollowed.id==post.user.id:
              result.append(post)
  paginator=Paginator(result,10)
  pn=request.GET.get('page')
  pageItems=paginator.get_page(pn)
  return render(request, "network/following.html", {'allPosts':pageItems})