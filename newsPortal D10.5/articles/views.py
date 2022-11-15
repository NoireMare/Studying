from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from news.models import Post
from news.forms import PostForm


class ArticleList(ListView):
    model = Post
    ordering = '-time_add'
    template_name = 'articles.html'
    context_object_name = 'articles'
    queryset = Post.objects.filter(type=False).order_by('-time_add')
    paginate_by = 10


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'articles'


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'articles/create.html'


class ArticleEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'articles/create.html'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'articles/delete.html'
    success_url = reverse_lazy('articles')
