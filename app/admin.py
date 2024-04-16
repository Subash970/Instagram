from django.contrib import admin
from .models import UserBio , UserFriends , Post , UserTable , Comments

# Register your models here.

admin.site.register(UserBio)
admin.site.register(UserFriends)
admin.site.register(Post)
admin.site.register(UserTable)
admin.site.register(Comments)