from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Author
from .forms import CreatePost

# Create your views here.
def index(request):
    posts=Post.objects.all()[0:3]
    context={
        'object':posts
    }
    return render(request,'blog/index.html',context)

def blogs(request):
    posts = Post.objects.all()
    context = {
        'object': posts
    }
    return render(request,'blog/blog.html',context)

def post(request,id):
    post=get_object_or_404(Post,id=id)
    context = {
        'object': post
    }
    return render(request,'blog/post.html',context)


@login_required
def create_post(request):
    author_=Author.objects.get(user=request.user)
    if author_ is None:
        messages.warning(request,"Sorry You are not allow to write the post")
        return redirect('index')
    form=CreatePost()
    if request.method=="POST":
        form=CreatePost(request.POST or None, request.FILES or None)
        if form.is_valid():
            post=form.save(commit=True)
            post.author=author_
            post.save()
            messages.warning(request,'You Post Has Been Created')
            return redirect('index')

    context={
        "form":form
    }
    return render(request,'blog/create-post.html',context)


# def update_post(request,id):
#