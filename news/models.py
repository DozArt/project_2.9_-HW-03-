from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        r = 0
        r1 = Post.objects.filter(author_id=self.id).values('rating', 'id')
        r += sum([i['rating'] for i in r1])  # суманрый рейтинг каждой статьи автора
        r *= 3
        r2 = Comment.objects.filter(user_id=self.id).values('rating')
        r += sum([i['rating'] for i in r2])  # суманрый рейтинг всех комментариев автора
        r3 = Comment.objects.filter(post__author_id=self.id).values('rating')
        r += sum([i['rating'] for i in r3])  # суманрый рейтинг всех коментариев к статьям автора
        self.rating = r
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    news = 'N'
    article = 'A'

    ESSENCE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    essence = models.CharField(max_length=1,
                               choices=ESSENCE,
                               default=news)
    date = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.text[:124]+'...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()