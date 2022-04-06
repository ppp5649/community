from django.contrib import admin
from board.models import Post, Comment, Photo


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'writer',
                    'created_at', 'updated_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_contents', 'comment_writer',
                    'created_at', 'updated_at')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('img',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Photo, PhotoAdmin)
