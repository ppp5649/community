from django.contrib import admin
from .models import BoardMember


class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password',
                    'created_at', 'updated_at')


admin.site.register(BoardMember, BoardMemberAdmin)

# Register your models here.
