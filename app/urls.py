from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('' , views.index , name='index'),
    path('explore/' , views.explore , name='explore'),
    path('reels/' , views.reels , name='reels'),
    path('inbox/' , views.inbox , name='inbox'),
    path('signup/' , views.signup , name='signup'),
    path('login/' , views.login , name='login'),
    path('logout/' , views.logout , name='logout'),
    path('userbio/' , views.userbio , name='userbio'),
    path('follow/' , views.follow , name='follow'),
    path('unfollow/' , views.unfollow , name='unfollow'),
    path('remove/' , views.remove , name='remove'),
    path('search/' , views.search , name='search'),
    path('add/' , views.add , name='add'),
    path('like/' , views.like , name='like'),
    path('save/' , views.save , name='save'),
    path('delete_post/' , views.delete_post , name='delete_post'),
    path('new_comment/' , views.new_comment , name='new_comment'),
    path('<str:pk>/followers/' , views.followers , name='followers'),
    path('<str:pk>/following/' , views.following , name='following'),
    path('p/<int:pk>/' , views.p , name='p'),
    path('<str:pk>/saved/' , views.saved , name='saved'),
    path('<str:pk>/liked/' , views.liked , name='liked'),
    path('p/<int:pk>/comment/' , views.comment , name='comment'),
    path('<str:pk>/' , views.profile , name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)