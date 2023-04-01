from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(profile)
admin.site.register(post)
admin.site.register(likepost)
admin.site.register(Comment)
admin.site.register(followerscount)
admin.site.register(Notification)
admin.site.register(Video)