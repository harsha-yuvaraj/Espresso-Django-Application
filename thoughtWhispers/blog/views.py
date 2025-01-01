from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

def post_list(request):
    all_posts = Post.published.all()
    # Pagination with 4 posts per page
    paginator = Paginator(all_posts, 4)
    page_number = request.GET.get('page', 1) # get the page number from the request, default to 1.
    
    try:
       posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, load the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, load the last page
        posts = paginator.page(paginator.num_pages)

    return render(
                request, 
                'blog/post/list.html', 
                {'posts': posts}
            )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(
                request, 
                'blog/post/detail.html', 
                {'post': post}
            )


