from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Author,Category,Tag,Comment
from .forms import CreatePostForm,UpdatePostForm,CommentForm

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
    cats=Category.objects.all()
    tags=Tag.objects.all()
    posts = Post.objects.all()

    # post_count_per_tag=Post.objects.filter()

    latest= Post.objects.order_by('-date_posted')[0:3]
    context = {
        'object': posts,
        'latest':latest,
        'cats':cats,
        'tags':tags,
    }
    return render(request,'blog/blog.html',context)

def post_detail(request, id):
    cats=Category.objects.all()
    tags=Tag.objects.all()

    post=get_object_or_404(Post,id=id)
    latest= Post.objects.order_by('-date_posted')[0:3]

    comments=Comment.objects.filter(post__id=id)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment=comment_form.save(commit=False)
            user_comment.post=post
            user_comment.save()
            return redirect('post',id=id)


    # cat_post=Post.objects.filter

    context = {
        'object': post,
        'latest':latest,
        'cats':cats,
        'tags':tags,

        # COMMENTS
        'comments':comments,
        'comment_form':comment_form,

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
            post=form.save(commit=False)
            post.author=author_
            post.save()
            messages.warning(request,'You Post Has Been Created')
            return redirect('index')

    context={
        "form":form
    }
    return render(request,'blog/create-post.html',context)


def update_post(request,id):
    author_=Author.objects.get(user=request.user)
    post=Post.objects.get(id=id)

    if post.author.user != request.user:
        messages.warning(request, "Restricted ..!")
        return redirect('index')

    if request.method == "POST":
        update_form = UpdatePostForm(request.POST or None, request.FILES or None,instance=post)
        if update_form.is_valid():
            post_ = update_form.save(commit=False)
            post_.save()
            post=post_
            messages.warning(request, f'{post.title} Has Been Updated')
            # return redirect('post',id=id)
            return redirect('blogs')

    form=UpdatePostForm(
        initial={
            "title":post.title,
            "content":post.content,
            "thumbnail":post.thumbnail,

    })
    context = {
        "form": form
    }
    return render(request, 'blog/update-post.html', context)
def delete_post(request,id):
    author_ = Author.objects.get(user=request.user)
    post = Post.objects.get(id=id)

    if post.author.user != request.user:
        messages.warning(request, "Restricted ..!")
        return redirect('post',id=id)
    post.delete()
    messages.success(request, f"{post.title} is successfully deleted ")
    return redirect('blogs')


def cat_detail(request,id):
    cat=get_object_or_404(Category,id=id)
    posts=Post.objects.filter(cat=cat)

    cats = Category.objects.all()
    tags = Tag.objects.all()
    latest = Post.objects.order_by('-date_posted')[0:3]

    context={
        'object':posts,
        'cat':cat,
        'latest': latest,
        'cats': cats,
        'tags': tags,
    }
    return render(request,'blog/cat-detail.html',context)

def tag_detail(request,id):
    tag=get_object_or_404(Tag,id=id)
    posts=Post.objects.filter(tag=tag)

    cats = Category.objects.all()
    tags = Tag.objects.all()
    latest = Post.objects.order_by('-date_posted')[0:3]
    context={
        'object':posts,
        'tag':tag,
        'latest': latest,
        'cats': cats,
        'tags': tags,
    }
    return render(request,'blog/tag-detail.html',context)


def search_function(request):
    post=Post.objects.all()
    title_contains_query = request.GET.get('search')
    if title_contains_query !='' and title_contains_query is not None:
        post=post.filter(title__icontains=title_contains_query)
    context={
        'object':post,
        'search_query':title_contains_query
    }
    return render(request,'blog/blog.html',context)
