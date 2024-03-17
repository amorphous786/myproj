from django.views.generic import ListView
from .models import Post
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail
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
def post_list(request):
  posts_list = Post.objects.all()
  paginator = Paginator(posts_list,5)
  page_number = request.GET.get('page',1)
  breakpoint()
  try:
    posts = paginator.page(page_number)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)
  except PageNotAnInteger:
    posts = paginator.page(1)
  return render(request,'blog/post/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
  post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           published__year=year,
                           published__month=month,
                           published__day=day)
  return render(request,
                'blog/post/detail.html',
                {'post':post})

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