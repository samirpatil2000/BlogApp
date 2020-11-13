from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Author,Category,Tag,Comment,LikePost,DislikePost
from .forms import CreatePostForm,UpdatePostForm,CommentForm,ImageForm

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
    latest = Post.objects.order_by('-date_posted')[0:3]

    # post_count_per_tag=Post.objects.filter()

    title_contains_query = request.GET.get('search')
    if title_contains_query != '' and title_contains_query is not None:
        posts = posts.filter(title__icontains=title_contains_query)


    context = {
        'object': posts,
        'latest':latest,
        'cats':cats,
        'tags':tags,
        'search_query': title_contains_query
    }
    return render(request,'blog/blog.html',context)

def post_detail(request, id):

    cats=Category.objects.all()
    tags=Tag.objects.all()

    post=get_object_or_404(Post,id=id)
    latest= Post.objects.order_by('-date_posted')[0:3]

    author=post.author.user

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
        'author':author,

        # COMMENTS
        'comments':comments,
        'comment_form':comment_form,

    }

    if request.user.is_authenticated:
        if LikePost.objects.filter(post=post, user=request.user).exists():
            context['is_like']='active'
        if DislikePost.objects.filter(post=post, user=request.user).exists():
            context['is_dislike']='active'

    return render(request,'blog/post-detail.html',context)


@login_required
def create_post(request):
    author_=Author.objects.get(user=request.user)


    if author_ is None:
        messages.warning(request,"Sorry You are not allow to write the post")
        return redirect('index')

    # imageform = ImageForm()


    form=CreatePostForm()
    if request.method=="POST":
        # imageform = ImageForm(request.POST or None, request.FILES or None)
        # if imageform.is_valid():
        #     imageform.save()
        form=CreatePostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=author_
            post.save()
            messages.warning(request,'You Post Has Been Created')
            return redirect('index')

    context={
        "form":form,
        # "imageform":imageform,
    }
    return render(request,'blog/create-post.html',context)

# def add_image(request):
#     imageform = ImageForm()
#     if request.method == "POST":
#         imageform = ImageForm(request.POST or None, request.FILES or None)
#         if imageform.is_valid():
#             imageform.save()
#

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


@login_required
def like_post(request,id):
    post=Post.objects.get(id=id)

    # like_post=LikePost.objects.get(post=post,user=request.user)
    # dislike_post=DislikePost.objects.get(post=post,user=request.user)


    if LikePost.objects.filter(post=post,user=request.user).exists():
        like_remove=LikePost.objects.get(post=post,user=request.user).delete()
        # like_remove.save()

    if DislikePost.objects.filter(post=post,user=request.user).exists():
        dislike_remove = DislikePost.objects.get(post=post, user=request.user).delete()
        # dislike_remove.save()

    LikePost.objects.create(post=post,user=request.user)
    return redirect('post',id=id)

@login_required
def dislike_post(request,id):
    post=Post.objects.get(id=id)

    #like_post = LikePost.objects.get(post=post, user=request.user)
    # dislike_post=DislikePost.objects.get(post=post,user=request.user)

    if DislikePost.objects.filter(post=post,user=request.user).exists():
        like_remove=DislikePost.objects.get(post=post,user=request.user).delete()
        # like_remove.save()

    if LikePost.objects.filter(post=post, user=request.user).exists():
        like_remove=LikePost.objects.get(post=post,user=request.user).delete()
        # like_remove.save()

    DislikePost.objects.create(post=post,user=request.user)
    # dislike.save()
    return redirect('post',id=id)

@login_required
def save_post(request,id):
    post =Post.objects.get(id=id)
    posts=Post.objects.filter(id=id,is_save=request.user)

    if posts.exists():
        messages.warning(request, "Post is remove from save")
        post.is_save.remove(request.user)
        post.save()
    else:
        messages.info(request,"Post is saved")
        post.is_save.add(request.user)
        post.save()

    return redirect('post',id=id)

