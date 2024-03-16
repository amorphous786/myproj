from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.http import Http404
# Create your views here.


def post_list(request):
  posts = Post.objects.all()
  return render(request,'blog/post/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
  # try:
  #   post = Post.objects.get(id=id)
  # except Post.DoesNotExist:
  #   raise Http404
  # return render(request,
  #               'blog/post/detail.html',
  #               {'post':post})
  post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           published__year=year,
                           published__month=month,
                           published__day=day)
  return render(request,
                'blog/post/detail.html',
                {'post':post})

