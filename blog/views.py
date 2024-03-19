from django.views.generic import ListView
from .models import Post,Comment
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
import os
from dotenv import load_dotenv
load_dotenv()
#Class based view for posts lists
# class PostListView(ListView):
#   queryset = Post.published_posts.all()
#   context_object_name = "posts"
#   paginate_by = 3
#   template_name = 'blog/post/list.html'
# function based view for posts lists
def post_list(request,tag_slug=None):
  posts_list = Post.objects.all()
  
  page_number = request.GET.get('page',1)
  tag = None
  if tag_slug:
    tag = get_object_or_404(Tag,slug=tag_slug)
    posts_list = posts_list.filter(tags__in=[tag])
  paginator = Paginator(posts_list,5)
  try:
    posts = paginator.page(page_number)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)
  except PageNotAnInteger:
    posts = paginator.page(1)
  return render(request,'blog/post/list.html',{'posts':posts,'tag':tag})

def post_detail(request,year,month,day,post):
  post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           published__year=year,
                           published__month=month,
                           published__day=day)
  comments = post.comments.filter(active=True)
  form = CommentForm()
  return render(request,
                'blog/post/detail.html',
                {'post':post,
                 'comments':comments,
                 'form':form})

def post_share(request,post_id):
  post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
  if request.method=='POST':
    form = EmailPostForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data 
      post_url = request.build_absolute_uri(post.get_absolute_url())
      subject = f"{cd['name']} recommends you read "\
                f"{post.title}"
      message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comments:{cd['comments']}"

      send_mail(subject,message,os.environ.get('EMAIL'),[cd['to']])
      sent = True
  else:
    sent=False
    form = EmailPostForm()
  return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})

@require_POST
def post_comment(request,post_id):
  post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
  comment = None
  form = CommentForm(data=request.POST)
  if form.is_valid():
    comment = form.save(commit=False)
    comment.post = post
    comment.save()

  return render(request,'blog/post/comment.html',
                {'post':post,
                 'form':form,
                 'comment':comment})