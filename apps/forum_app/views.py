from django.shortcuts import render, redirect
from .models import Post
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    
    threads = Post.objects.filter(is_thread=True).order_by('updated_at')

    for thread in threads:
        num = len(thread.replies.all())
        thread.abridged_replies = list(thread.replies.all())[-2:]
        if num > 2:
            thread.hidden = num - 2

    return render(request, "forum_app/index.html", {"posts": threads})

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
    return render(request, "forum_app/thread.html", {"post": Post.objects.get(id=thread_id)})

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
    print("path")
    return render(request, "forum_app/404.html")