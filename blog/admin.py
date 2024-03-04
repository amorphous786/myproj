from django.contrib import admin
from blog.models import Post
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