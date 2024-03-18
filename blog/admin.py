from django.contrib import admin
from blog.models import Post,Comment
# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ['title','slug','author','published','status']
  list_filter = ['published','status','created','author']
  search_fields = ['title','body','slug']
  prepopulated_fields = {'slug':('title',)}
  raw_id_fields = ['author']
  date_hierarchy = 'published'
  ordering = ['status','published']
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ['name','email','body','active','created','updated']
  list_filter = ['name','created','active','post']
  search_fields = ['name','body','email']
  # raw_id_fields = ['post']
  date_hierarchy = 'created'
  ordering = ['-created']