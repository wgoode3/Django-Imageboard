from django.shortcuts import render, redirect
from .models import Post

def index(request):
	
	threads = Post.objects.filter(is_thread=True)

	for thread in threads:
		num = len(thread.replies.all())
		thread.abridged_replies = list(thread.replies.all())[-3:]
		if num > 3:
			thread.hidden = num - 3

	return render(request, "forum_app/index.html", {"posts": threads})

def new_thread(request):
	print(Post.objects.new_thread(request.POST, request.FILES))
	return redirect("/")

def reply(request, post_id):
	print(Post.objects.new_reply(request.POST, request.FILES, post_id))
	return redirect("/")

def thread(request, thread_id):
	return render(request, "forum_app/thread.html", {"post": Post.objects.get(id=thread_id)})