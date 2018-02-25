from django.shortcuts import render, redirect
from .models import Post
from django.contrib import messages

def index(request):
	
	threads = Post.objects.filter(is_thread=True)

	for thread in threads:
		num = len(thread.replies.all())
		thread.abridged_replies = list(thread.replies.all())[-3:]
		if num > 3:
			thread.hidden = num - 3

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