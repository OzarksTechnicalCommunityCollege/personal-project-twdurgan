from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm
from .models import Post

# Post Views

# class PostListView(ListView):
#     queryset = Post.viewable.all()
#     context_object_name = 'posts'
#     paginate_by = 25
#     template_name = 'booru/post/list.html'
    # Implementation of features mentioned below in the function-based post list view could be handled with class methods that are referenced in class variable definitions.
    # I would prefer to use this as it seems to keep code concise, however I don't know a way to manage pagination exception handling in class-based views yet.

def post_view(request, id):
    try:
        post = Post.viewable.get(id=id)
    except Post.DoesNotExist:
        raise Http404('Post not found.')
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        'booru/post/view.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        }
    )

def post_list(request):
    post_list = Post.viewable.all()
    # When implementing extra-fancy features, might be able to get the number of posts paginated to adjust
        # based upon the viewport size of the user at the time of navigation.
    paginator = Paginator(post_list, 25)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Low-priority: could hide some fun easter eggs here, like allowing page inputs in hex codes
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'booru/post/list.html', {'posts': posts})

# Originally, this was going to allow for any viewable post to have requests made for it, but using the viewable manager for get_object_or_404 doesn't work.
# On further consideration though, the manual review period for a post is the point where many changes that would be requested would be made, e.g. deleting inferior duplicate posts.
# As a result, requests are only going to be implemented on approved posts, being that their functional role is to catch and report mistakes made in the manual review process, which unapproved-but-viewable have not gone through.
def post_request(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        # TODO: Make alternate message subjects depending upon if the "name" field for the form was filled, as it currently is not used.
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f'Request for post {post.id} ({cd['email']}: {cd['subject']})')
            message = (f"Request text: {cd['request']}\n\nPost Link: {post_url}")
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=['winnow@jacka.lope']
            )
            sent=True
    else:
        form = EmailPostForm()
    return render(
        request,
        'booru/post/request.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

# Same problem as the above request form, only this time I do actually want every viewable post to have comments available.
# This will probably involve looking at the return for get_object_or_404 and setting up logic to make different objects depending on if the post is published, since the status parameter doesn't seem to like receiving multiple arguments.

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        'booru/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )