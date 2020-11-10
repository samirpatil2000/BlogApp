from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Author
from .forms import CreatePostForm,UpdatePostForm

# Create your views here.
def index(request):
    posts=Post.objects.all()[0:3]
    latest = Post.objects.order_by('-date_posted')[0:3]
    context={
        'objects':posts,
        'latest':latest,
    }
    return render(request,'blog/index.html',context)

def blogs(request):
    posts = Post.objects.all()
    latest= Post.objects.order_by('-date_posted')
    context = {
        'object': posts,
        'latest':latest,
    }
    return render(request,'blog/blog.html',context)

def post_detail(request, id):
    post=get_object_or_404(Post,id=id)
    latest= Post.objects.order_by('-date_posted')[0:3]
    context = {
        'object': post,
        'latest':latest
    }
    return render(request,'blog/post-detail.html',context)


@login_required
def create_post(request):
    author_=Author.objects.get(user=request.user)
    if author_ is None:
        messages.warning(request,"Sorry You are not allow to write the post")
        return redirect('index')
    form=CreatePostForm()
    if request.method=="POST":
        form=CreatePostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post=form.save(commit=True)
            post.author=author_
            post.save()
            messages.warning(request,'You Post Has Been Created')
            return redirect('index')

    context={
        "form":form
    }
    return render(request,'blog/create-post-detail.html',context)


def update_post(request,id):
    post=Post.objects.get(id=id)

    if post.author.user == request.user:
        messages.warning(request, "Restricted ..!")
        return redirect('index')
    if request.method == "POST":
        update_form = UpdatePostForm(request.POST or None, request.FILES or None)
        if update_form.is_valid():
            post = update_form.save(commit=True)
            post.save()
            messages.warning(request, 'You Post Has Been Updated')
            return redirect('post',id=id)

    form=UpdatePostForm(
        initial={
            "title":post.title,
            "content":post.content,
            "thumbnail":post.thumbnail,

    })
    context = {
        "form": form
    }
    return render(request, 'blog/update-post-detail.html', context)