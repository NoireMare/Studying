from django.db import models
from django.contrib.auth.models import User

#  from news.models import Author, Post, Category, PostCategory, Comment, UserCategory
from django.urls import reverse


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.author}"

    @staticmethod
    def update_rating(value):
        try:
            total_posts_rating, total_comments_rating, total_comments_to_author_rating = 0, 0, 0
            posts_rating_list = Post.objects.filter(post_author=value, type=True).values("rating")
            for dict_ in posts_rating_list:
                total_posts_rating += dict_["rating"] * 3
            comments_rating_list = Comment.objects.filter(comment_who=Author.objects.get(pk=value).author).values("rating")
            for dict_ in comments_rating_list:
                total_comments_rating += dict_["rating"]
            values_list = Post.objects.filter(post_author=Author.objects.get(pk=value).id).values("id")
            for val in values_list:
                comm_by_author = Comment.objects.filter(comment_to_post=val["id"]).values("rating")
                for comms in comm_by_author:
                    total_comments_to_author_rating += comms["rating"]
            rating_author = total_posts_rating + total_comments_rating + total_comments_to_author_rating
            author = Author.objects.get(pk=value)
            author.rating = Author.objects.get(pk=value).rating + rating_author
            author.save()
        except BaseException:
            print("Указанного автора нет в базе")


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    category_user = models.ManyToManyField(User, through="UserCategory")

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.BooleanField(default=False)
    time_add = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField(default=0)

    category_post = models.ManyToManyField(Category, through='PostCategory')

    def get_absolute_url(self):
        if self.type:
            return reverse('post_detail', args=[self.id])
        else:
            return reverse('article_detail', args=[self.id])

    @staticmethod
    def like(value):
        try:
            post = Post.objects.get(pk=value)
            post.rating += 1
            post.save()
        except BaseException:
            print("Запрошенный пост не найден")

    @staticmethod
    def dislike(value):
        try:
            post = Post.objects.get(pk=value)
            post.rating -= 1
            post.save()
        except BaseException:
            print("Запрошенный пост не найден")

    @staticmethod
    def preview(value):
        try:
            post_preview = Post.objects.get(pk=value).text
            print(post_preview[:124] + "...")
        except BaseException:
            print("Запрошенный пост не найден")


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_who = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_add = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    @staticmethod
    def like(value):
        try:
            comment = Comment.objects.get(pk=value)
            comment.rating += 1
            comment.save()
        except BaseException:
            print("Запрошенный комментарий не найден")

    @staticmethod
    def dislike(value):
        try:
            comment = Comment.objects.get(pk=value)
            comment.rating -= 1
            comment.save()
        except BaseException:
            print("Запрошенный комментарий не найден")
