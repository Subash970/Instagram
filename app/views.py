from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User , auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import UserBio , UserFriends , Post , UserTable , Comments
from .forms import UserBioForm , PostForm , CommentForm
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import datetime
from datetime import  timedelta

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    auth_user_bio = None
    try:
        auth_user_bio = UserBio.objects.get(user = request.user)
    except ObjectDoesNotExist:
        pass

    posts = Post.objects.all().order_by('upload_at').reverse()
    post_info = []

    for i in posts:
        try:
            follower = UserBio.objects.get(user = i.user)
            comment = Comments.objects.filter(post = i).count()
            post_info.append({'post' : i , 'bio_img' : follower.img ,  'comment' : comment})
        except ObjectDoesNotExist:
            post_info.append({'post' : i , 'bio_img' : '' ,  'comment' : comment})
  

    user_table = None
    try:
        user_table = UserTable.objects.get(user = request.user)
    except ObjectDoesNotExist:
        pass

    context = {
        'auth_user_bio' : auth_user_bio,
        'user_table' : user_table,
        'post_info' : post_info,
    }
    return render(request , 'index.html' , context)

@login_required(login_url='/login/')
def explore(request):
    auth_user_bio = None
    try:
        auth_user_bio = UserBio.objects.get(user = request.user)
    except ObjectDoesNotExist:
        pass

    posts = Post.objects.all().order_by('upload_at').reverse()

    context = {
        'auth_user_bio' : auth_user_bio,
        'posts' : posts,
    }
    return render(request , 'explore.html' , context)


def search(request):
    if request.method == 'POST':
        user = request.POST['user']    
        search_result_info = []
        try:
            search_result = User.objects.filter(username__icontains=user)
            for i in search_result:
                try:
                    follower = UserBio.objects.get(user = i)
                    search_result_info.append({'user' : i , 'username' : follower.username , 'img' : follower.img})
                except ObjectDoesNotExist:
                    search_result_info.append({'user' : i , 'username' : '' , 'img' : ''})
            
        except User.DoesNotExist:
            messages.info(request , 'No results found')
            return redirect('search')
        
        context = {
            'search_result_info' : search_result_info,
        }
        return render(request , 'search.html' , context)
    else:
        return render(request , 'search.html')
    

@login_required(login_url='/login/')
def inbox(request):
    return render(request , 'inbox.html')

@login_required(login_url='/login/')
def reels(request):
    auth_user_bio = None
    try:
        auth_user_bio = UserBio.objects.get(user = request.user)
    except ObjectDoesNotExist:
        pass

    context = {
        'auth_user_bio' : auth_user_bio
    }
    return render(request , 'reels.html' , context)


def profile(request , pk):
    try:
        user = User.objects.get(username = pk)
        user_bio_form = UserBioForm()

        auth_user_check = user == request.user

        user_bio = None
        user_posts = None
        try:
            user_bio = UserBio.objects.get(user = user)
            user_posts = Post.objects.filter(user = user).reverse()
        except ObjectDoesNotExist:
            pass 

        auth_user_bio = None
        if request.user.is_authenticated:
            try:
                auth_user_bio = UserBio.objects.get(user = request.user)
            except ObjectDoesNotExist:
                pass

        user_friends = None
        user_friends_followers = None
        user_friends_following = None
        following = None
        try:
            user_friends = UserFriends.objects.get(user = user)
            user_friends_followers = user_friends.followers.all()
            user_friends_following = user_friends.following.all()
            if request.user.is_authenticated:
                auth_user_friends = UserFriends.objects.get(user=request.user)
            
                if user in auth_user_friends.following.all():
                    following = True
                else:
                    following = False

        except ObjectDoesNotExist:
            pass

        context = {
            'user_bio_form' : user_bio_form,
            'auth_user_bio' : auth_user_bio,
            'user_bio' : user_bio,
            'auth_user_check' : auth_user_check,
            'user' : user,
            'user_friends' : user_friends,
            'user_friends_followers' : user_friends_followers,
            'user_friends_following' : user_friends_following,
            'following' : following,
            'user_posts' : user_posts,
        }
        return render(request , 'profile.html' , context)
    except User.DoesNotExist:
        return HttpResponse("User does'nt available")
    


@login_required(login_url='/login/')
def following(request,pk):
    user = get_object_or_404(User , username = pk)
    user_friends = None
    user_friends_following = None
    user_friends_following_bio = None
    try:
        user_friends = UserFriends.objects.get(user = user)
        user_friends_following = user_friends.following.all()
        user_friends_following_bio = []

        auth_user_friends = UserFriends.objects.get(user = request.user)
        auth_user_friends_following = auth_user_friends.following.all()

        auth_user_friends = UserFriends.objects.get(user = request.user)

        for i in user_friends_following:
            try:
                follower_bio = UserBio.objects.get(user = i)
                user_friends_following_bio.append({'user' : follower_bio.user , 'username' : follower_bio.username, 'img' : follower_bio.img}) 
            except ObjectDoesNotExist:
                user_friends_following_bio.append({'user' : i , 'username' : '' , 'img' : ''})

    except ObjectDoesNotExist:
        pass
    context = {
        'user_friends' : user_friends,
        'user_friends_following' : user_friends_following ,
        'user_friends_following_bio' : user_friends_following_bio,
        'auth_user_friends_following' : auth_user_friends_following,
    }
    return render(request , 'following.html' , context)


@login_required(login_url='/login/')
def followers(request , pk):
    user = User.objects.get(username = pk)
    user_friends = None
    user_friends_followers = None
    user_friends_following = None
    auth_user_friends = None
    auth_user_check = user == request.user

    try:
        user_friends = UserFriends.objects.get(user = user)
        user_friends_followers = user_friends.followers.all()
        auth_user_friends = UserFriends.objects.get(user = request.user)
        auth_user_friends_following = auth_user_friends.following.all()

        user_friends_followers_bio = []
        for i in user_friends_followers:
            try:
                follower_bio = UserBio.objects.get(user = i)
                user_friends_followers_bio.append({'user' : follower_bio.user , 'username' : follower_bio.username , 'img' : follower_bio.img})
            except ObjectDoesNotExist:
                user_friends_followers_bio.append({'user' : i , 'username' : '' , 'img' : ''})

    except ObjectDoesNotExist:
        pass
    context = {
        'user' : user,
        'user_friends' : user_friends,
        'user_friends_followers' : user_friends_followers,
        'user_friends_followers_bio' : user_friends_followers_bio ,
        'auth_user_check' : auth_user_check ,
        'auth_user_friends_following' : auth_user_friends_following,
    }
    return render(request , 'followers.html' ,context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request , 'Username already taken')
                return redirect('signup')
            else:
                new_user = User.objects.create_user(username=username , password=password1)
                new_user.save()
                auth_login = auth.authenticate(username = username , password = password1)
                auth.login(request , auth_login)
                return redirect('/')
        else:
            messages.info(request , "Password did'nt match")
            return redirect('signup')
    else:
        return render(request , 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth_login = auth.authenticate(username = username , password = password)
        if auth_login is not None:
            auth.login(request , auth_login)
            return redirect('/')
        else:
            messages.info(request , 'Invalid credentials')
            return redirect('login')
    else:
        return render(request , 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def userbio(request):
    if request.method == 'POST':
        userbioinfo = UserBioForm(request.POST , request.FILES)

        if userbioinfo.is_valid():
            username = userbioinfo.cleaned_data['username']
            bio = userbioinfo.cleaned_data['bio']
            img = userbioinfo.cleaned_data['img']
            user = request.user

            userbio_instance,_ = UserBio.objects.get_or_create(user=user)

            if bio:
                userbio_instance.bio = bio
            if username:
                  userbio_instance.username = username
            if img:
                userbio_instance.img = img
            userbio_instance.save()
            return redirect('profile' , user)


@login_required(login_url='/login/')
def follow(request):
    if request.method == 'POST':
        user =  request.POST['user']
        username = get_object_or_404(User , username=user)
        auth_user = request.user

        username_friends, _ = UserFriends.objects.get_or_create(user = username)
        auth_user_friends, _ =UserFriends.objects.get_or_create(user=auth_user)

        if username in auth_user_friends.following.all():
            auth_user_friends.following.remove(username)
            username_friends.followers.remove(auth_user)
        else:
            auth_user_friends.following.add(username)
            username_friends.followers.add(auth_user)

        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login/')  
def remove(request):
    if request.method == 'POST':
        user = request.POST['user']
        username = User.objects.get(username=user)
        username_followers = UserFriends.objects.get(user = username)
        auth_user_followers = UserFriends.objects.get(user=request.user)
        if username in auth_user_followers.followers.all():
            auth_user_followers.followers.remove(username)
            username_followers.following.remove(request.user)
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponse("There is an error occured")

@login_required(login_url='/login/')
def unfollow(request):
    if request.method == 'POST':
        user = request.POST['user']
        username = get_object_or_404(User , username = user)
        user_friends = UserFriends.objects.get(user = username)
        auth_user_friends = UserFriends.objects.get(user = request.user)

        if username in auth_user_friends.following.all():
            auth_user_friends.following.remove(username)
            user_friends.followers.remove(request.user)
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponse("There is an error occured")
        

@login_required(login_url='/login/')
def add(request):
    if request.method == 'POST':
        new_post = PostForm(request.POST , request.FILES)
        if new_post.is_valid():
            instance = new_post.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('/')
    else:
        postform = PostForm()
        context = {
            'postform' : postform,
        }
        return render(request , 'add.html' , context)
    

@login_required(login_url='/login/')
def p(request , pk):
    post = get_object_or_404(Post , id = pk)
    post_comments = None

    try:
        post_comments = Comments.objects.filter(post = post).count()
    except ObjectDoesNotExist:
        pass

    post_user = None
    user_table = None
    try:
        post_user = UserBio.objects.get(user = post.user)
        user_table = UserTable.objects.get(user = request.user)
    except ObjectDoesNotExist:
        pass

    context = {
        'post' : post ,
        'user_table' : user_table,
        'post_user' : post_user,
        'post_comments' : post_comments,
    }
    return render(request , 'p.html' , context)


@login_required(login_url='/login/')
def like(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post , id=post_id)
        auth_user_like,_ = UserTable.objects.get_or_create(user = request.user)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            auth_user_like.liked.remove(post)
        else:
            post.likes.add(request.user)
            auth_user_like.liked.add(post)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login/')
def saved(request , pk):
    user = request.user
    user_saved = None
    saved_posts = None
    try:
        user_saved = UserTable.objects.get(user=user)
        saved_posts = user_saved.saved.all()
    except ObjectDoesNotExist:
        pass

    context = {
        'user_saved' : user_saved,
        'saved_posts' : saved_posts,
    }
    return render(request , 'saved.html' , context)


@login_required(login_url='/login/')
def save(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)
        user_table,_ = UserTable.objects.get_or_create(user = request.user)

        if post in user_table.saved.all():
            user_table.saved.remove(post)
        else:
            user_table.saved.add(post)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login/')
def comment(request , pk):
    post = get_object_or_404(Post , id=pk)
    commentform = CommentForm()
    post_comments_get = None
    post_comments = []

    try:
        post_comments_get = Comments.objects.filter(post = post)
        
        for i in post_comments_get:
            user = UserBio.objects.get(user = i.user)
            try:
                post_comments.append({'post_comments' : i , 'user_img' : user.img})
            except ObjectDoesNotExist:
                post_comments.append({'post_comments' : i , 'user_img' : ''})

    except ObjectDoesNotExist:
        pass

    context = {
        'post_comments_get' : post_comments_get,
        'post_comments' : post_comments,
        'commentform' : commentform,
        'post' : post,
    }
    return render(request , 'comment.html' , context)


@login_required(login_url='/login/')
def new_comment(request):
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        post_id = request.POST['post']
        post = get_object_or_404(Post , id=post_id)
        if comment.is_valid():
            instance = comment.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        

def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post , id=post_id)
        post.delete()
        return redirect('profile' , request.user)
    
def liked(request , pk):
    user = request.user
    user_table = None
    liked_post = None
    try:
        user_table = UserTable.objects.get(user=user)
        liked_post = user_table.liked.all()
    except ObjectDoesNotExist:
        pass

    context = {
        'liked_post' : liked_post,
        'user_table' : user_table,
    }
    return render(request , 'liked.html' , context)