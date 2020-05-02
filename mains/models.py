from django.contrib.auth.models import AbstractUser, BaseUserManager, \
    PermissionsMixin
from django.db import models
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(
            self,
            email,
            username,
            password,
    ):
        if not email:
            raise ValueError('ENTER AN EMAIL BUDDY')
        if not username:
            raise ValueError('I KNOW YOU HAVE A NAME')
        if not password:
            raise ValueError('PASSWORD?!?!?!? HELLO??')

        user = self.model(email=self.normalize_email(email),
                          username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            username,
            password,
    ):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class Members(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = []

    image = models.ImageField(upload_to='profile_image',
                              height_field=None, width_field=None,
                              max_length=None)

    object = UserManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @classmethod
    def creates(cls, username):
        username = cls(username=username)
        return username


class Profile(models.Model):
    id = (models.ForeignKey(Members, on_delete=models.CASCADE,
                            primary_key=True),)
    username = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    insta_id = models.CharField(max_length=50)
    about = models.CharField(max_length=500)
    image = models.ImageField(upload_to='profile_image', default=0)

    @classmethod
    def profile_pic(cls, username):
        profile = Profile.objects.get(username=username)
        return profile.image.url

    @classmethod
    def create(cls, username):
        username = cls(username=username)
        return username


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=50)
    author_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    edit = models.BooleanField(default=False)
    comment_no = models.PositiveIntegerField(default=0)
    user_pic = models.URLField()

    @classmethod
    def create(cls, i):
        cls.id = 4

        # do something with the book

        return cls.id

    def comments(self):
        return Comment.objects.all().filter(blog_id=id)


class Comment(models.Model):
    blog_id = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    commenter = models.CharField(max_length=40)
    commenter_name = models.CharField(max_length=200, default='User')

    def name(self):
        return Members.objects.filter(username=self.commenter)
