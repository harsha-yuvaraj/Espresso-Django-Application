from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from .models import Post

"""
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
"""

# Class-based view for post list
class PostListView(ListView):
    queryset = Post.published.all()
    # The default variable is object_list if you don’t specify any context_object_name
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    # Note: Django’s ListView generic view passes the page requested in a variable called page_obj. Use that name for pagination handling in the template.
    # In-built exception handling: Also, If an attempt to load a page out of range or pass a non-integer value in the page parameter, the view will return an HTTP response with the status code 404 (page not found).

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # list of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to add comments
    form = CommentForm()

    return render(
                request, 
                'blog/post/detail.html', 
                {'post': post, 'comments': comments, 'form': form}
            )

def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    sent=False
    if request.method == 'POST': # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid(): # Form fields passed validation
           cd = form.cleaned_data
           # email logic
           post_url = request.build_absolute_uri(post.get_absolute_url())
           subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
           message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
           code =  send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,# uses Default email address
                    recipient_list=[cd['to']],
                   )

           sent= True if code==1 else False

    else: # GET request
        form = EmailPostForm()

    return render(
                request,
                'blog/post/share.html',
                {'post': post, 'form': form, 'sent': sent}
           )

@require_POST       
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    
    # create the form instance from POST returned data
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the current post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    return render(
                request,
                'blog/post/comment.html',
                {'post': post, 
                 'comment': comment, 
                 'form': form
                }
            )

