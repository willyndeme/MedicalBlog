from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from medblog.forms import PostForm
from medblog.models import Post


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-created_at')  # Get all posts ordered by creation date
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'index.html', {'page_obj': page_obj})


def posts(request):
    posts = Post.objects.all().order_by('-created_at')  # Get all posts ordered by creation date
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'post.html', {'page_obj': page_obj})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the logged-in user as the author
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('index')  # Replace with the name of your post list URL
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, 'action': 'Create'})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('index')  # Replace with the name of your post list URL
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'action': 'Update'})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('index')  # Replace with the name of your post list URL
    return render(request, 'post_confirm_delete.html', {'post': post})


def search_blogs(request):
    query = request.GET.get('q')  # Get the search query from the request
    results = Post.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'query': query, 'results': results})


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog_detail.html', {'post': post})