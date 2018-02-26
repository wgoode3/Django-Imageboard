from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import Post
import math

PAGE_SIZE = settings.PAGE_SIZE

def index(request):

    # check which page of results to display
    try:
        p = int(request.GET["p"]) if "p" in request.GET else 1
    except ValueError:
        p = 1

    threads = Post.objects.filter(is_thread=True)
    pages = list(range(1,int(math.ceil(len(threads)/PAGE_SIZE))+1))

    # limit the results to the appropriate page
    indices = (0, PAGE_SIZE) if p==1 else ((p-1)*PAGE_SIZE, p*PAGE_SIZE)
    threads = threads.order_by('-updated_at')[indices[0]:indices[1]]

    # add abridged replies and number of hidden replies to the results
    for thread in threads:
        num = len(thread.replies.all())
        thread.abridged_replies = list(thread.replies.all())[-2:]
        if num > 2:
            thread.hidden = num - 2

    return render(request, "forum_app/index.html", {"posts": threads, "pages": pages})

def new_thread(request):
    post = Post.objects.new_thread(request.POST, request.FILES)
    if type(post) is list:
        for error in post:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def reply(request, post_id):
    post = Post.objects.new_reply(request.POST, request.FILES, post_id)
    if type(post) is list:
        for error in post:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/thread/{}".format(post_id))

def thread(request, thread_id):
    try:
        return render(request, "forum_app/thread.html", {"post": Post.objects.get(id=thread_id)})
    except ObjectDoesNotExist:
        full_path = "localhost:8000/thread/{}".format(thread_id)
        return render(request, "forum_app/404.html", {"path": full_path})

def query(request, post_id):
    post = Post.objects.filter(id=post_id)
    if len(post) == 0:
        url = "/not_found"
    elif post[0].is_thread:
        url = "/thread/{}#{}".format(post_id, post_id)
    else:
        url = "/thread/{}#{}".format(post[0].replies.all()[0].id, post_id)
    return JsonResponse({"url": url})

def not_found(request, path):
    full_path = "localhost:8000/{}".format(path)
    return render(request, "forum_app/404.html", {"path": full_path})