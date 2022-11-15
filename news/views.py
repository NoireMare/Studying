from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from news.tasks import send_emails_to_subscribers


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type=True).order_by('-time_add')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'


def news_filter(request):
    news = Post.objects.filter(type=True).order_by('-time_add')
    n_filter = PostFilter(request.GET, queryset=news)
    posts = n_filter.qs
    context = {
        'posts': posts,
        'n_filter': n_filter,
    }
    return render(request, 'news/search.html', context)


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'
    success_url = 'success'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = True
        return super().form_valid(form)

    def send_emails(self):
        post = Post.objects.all().last()
        title, text, id = [post.title, post.text, post.id]
        data = {'title': title, 'text': text, 'id': id}
        for cat in post.category_post.all():
            for subscriber in cat.category_user.all():
                data['subscriber_email'] = subscriber.email
                data['subscriber_username'] = subscriber.username
                send_emails_to_subscribers.delay(data)
        return redirect('/news')


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'
    permission_required = 'news.change_post'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('posts')
    permission_required = 'news.delete_post'


def posts_in_category(request, category_id):
    news = Post.objects.filter(type=True, category_post=category_id).order_by('-time_add')
    n_filter = PostFilter(request.GET, queryset=news)
    posts = n_filter.qs
    category = Category.objects.get(id=category_id)
    context = {
        'posts': posts,
        'n_filter': n_filter,
        'cat': category
    }
    return render(request, 'news_in_category.html', context)


class Categories(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'cats'











