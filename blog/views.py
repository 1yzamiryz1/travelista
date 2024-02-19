from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.forms import CommentForm
from blog.models import Post, Comment


def blog_view(request, **kwargs):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    if kwargs.get("cat_name") != None:
        posts = posts.filter(category__name=kwargs["cat_name"])
    if kwargs.get("author_username") != None:
        posts = posts.filter(author__username=kwargs["author_username"])
    if kwargs.get("tag_name") != None:
        posts = posts.filter(tags__name__in=[kwargs["tag_name"]])
    posts = Paginator(posts, 1)

    try:
        page_number = request.GET.get("page")
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {"posts": posts}
    return render(request, "blog/blog-home.html", context)


def blog_single(request, pid):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=pid)
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Your Comment Submitted Successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Your Comment Didnt Submitted')

    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    current_post = get_object_or_404(
        Post, pk=pid, status=1, published_date__lte=timezone.now()
    )
    current_post.counted_views += 1
    current_post.save()

    post_ids = [post.id for post in posts]

    current_index = post_ids.index(current_post.id)

    prev_post_id = post_ids[current_index - 1] if current_index > 0 else None
    next_post_id = (
        post_ids[current_index + 1] if current_index < len(post_ids) - 1 else None
    )

    prev_post = (
        get_object_or_404(
            Post, pk=prev_post_id, status=1, published_date__lte=timezone.now()
        )
        if prev_post_id
        else None
    )
    next_post = (
        get_object_or_404(
            Post, pk=next_post_id, status=1, published_date__lte=timezone.now()
        )
        if next_post_id
        else None
    )
    if not current_post.login_require:
        comments = Comment.objects.filter(post=current_post.id, approved=True)
        form = CommentForm()
        context = {
            "post": current_post,
            "prev_post": prev_post,
            "next_post": next_post,
            "comments": comments,
            "form": form
        }
        return render(request, "blog/blog-single.html", context)
    else:
        return redirect('accounts:login')


def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    posts = posts.filter(category__name=cat_name)
    context = {"posts": posts}
    return render(request, "blog/blog-home.html", context)


def blog_search(request):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    if request.method == "GET":
        if s := request.GET.get("s"):
            posts = posts.filter(content__contains=s)

    context = {"posts": posts}
    return render(request, "blog/blog-home.html", context)
