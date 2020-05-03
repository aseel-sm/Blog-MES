from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Members
from .models import Comment
from .models import Blog


def index(request):
    blogs = Blog.objects.order_by('-date')
    users = Members.objects.all()
    comments = Comment.objects.all()
    return render(request, 'blog_quick_view.html', {
        'blogs': blogs,
        'users': users,
        'comments': comments,
        'profile': Profile.profile_pic,
    })


def login(request):
    return render(request, 'login.html')


def about(request):
    return render(request, 'about.html')


def search(request, type):
    if type == 'profile':
        data = Members.objects.all()
    if type == 'post':
        data = Blog.objects.order_by('-date')
    return render(request, 'search.html', {'data': data, 'type': type})


def login_action(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(myprofile, username=username)
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect(login)
    return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect(index)


def read(request, blog_id):
    blog = Blog.objects.all().filter(id=blog_id)
    comments = Comment.objects.all().filter(blog_id=blog_id)
    return render(request, 'read_blog.html', {'blogs': blog,
                                              'comments': comments, 'id': blog_id})


def profile(request, username):
    user_data = Members.objects.all().filter(username=username)
    user_profile = Profile.objects.all().filter(username=username)
    user_blogs = Blog.objects.filter(author=username).order_by('-date')
    return render(request, 'profile.html', {
        'user_blogs': user_blogs,
        'user_data': user_data,
        'user_profile': user_profile,
        'username': username,
    })


@login_required
def myprofile(request, username):
    user_data = Members.objects.all().filter(username=username)
    user_profile = Profile.objects.all().filter(username=username)
    user = Members.creates(username)
    user_blogs = Blog.objects.filter(author=user).order_by('-date')
    return render(request, 'myprofile.html', {
        'user_blogs': user_blogs,
        'user_data': user_data,
        'user_profile': user_profile,
        'username': username,
    })


@login_required
def add_blog(request):
    return render(request, 'add_blog.html')


def sign_up(request):
    dept = [
        'Select',
        'Computer Application',
        'Business Administration',
        'Commerce',
        'Physics',
        'Electronics',
        'Arabic',
        'English',
        'Psychology',
        'Bio Science',
        'Mathematics and Stastics',
        'Animation and Graphic Design',
        'Fashion Design and Management',
        'Logistic Management',
        'Industrial Instrumention and Automation',
        'Software Development and System Administration',
        'Human Resource Management',
    ]

    return render(request, 'sign_up.html', {'dept': dept})


# adding new user

def sign_up_action(request):
    if request.method == 'POST' or request.FILES['profile']:
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        dept = request.POST['dept']
        email = request.POST['email']
        insta_id = request.POST['insta_id']
        about = request.POST['about']

        # fname,lname=fullname.split()

        try:
            users = Members.objects.get(username=username)
        except:
            users = None
        if users is not None:
            messages.error(request, ' Username already taken')
            return redirect(sign_up)

        if 'profile' in request.FILES:
            profile = request.FILES['profile']
        else:

            profile = 'default.png'

        new_user = Members.objects.create_user(username=username,
                                               password=password, first_name=fullname, email=email,
                                               image=profile)
        new_user.save()

        new_profile = Profile(username=username, dept=dept,
                              insta_id=insta_id, about=about)
        new_profile.save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return redirect(myprofile, username=username)
    else:
        return redirect(sign_up)


@login_required
def add_blog_action(request, user, name):
    if request.method == 'POST':
        content = request.POST['content']
        title = request.POST['title']
        profile = request.user.image
        new_blog = Blog(content=content, title=title, author=user,
                        author_name=name, user_pic=profile)
        new_blog.save()
        return redirect(myprofile, user)


@login_required
def edit_blog(request, id):
    blog = Blog.objects.get(pk=id)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        blog.title = title
        blog.content = content
        blog.edit = 1
        blog.save()
    return redirect(myprofile, username=request.user)


@login_required
def delete_blog(request, id):
    blog = Blog.objects.get(pk=id)
    blog.delete()
    return redirect(myprofile, username=request.user)


@login_required
def comment_blog(request, id):
    blog = Blog.objects.get(pk=id)
    if request.method == 'POST':
        comment = request.POST['comment']
        new_comment = Comment(comment=comment, blog_id=id,
                              commenter=request.user,
                              commenter_name=request.user.first_name)
        new_comment.save()
        no = blog.comment_no
        no = no + 1
        blog.comment_no = no
        blog.save()
    return redirect(read, blog_id=id)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST['username']

        fullname = request.POST['fullname']
        email = request.POST['email']
        insta_id = request.POST['insta_id']
        about = request.POST['about']

        request.user.email = email
        request.user.first_name = fullname
        request.user.save()

        profile = Profile.objects.get(pk=username)
        profile.insta_id = insta_id
        profile.about = about
        profile.save()
        return redirect(myprofile, username=username)
